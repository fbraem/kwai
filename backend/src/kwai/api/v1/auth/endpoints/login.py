"""Module that implements all APIs for login."""
from fastapi import APIRouter, Depends, status, HTTPException, Form, Response
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from loguru import logger
from pydantic import BaseModel

from kwai.api.dependencies import deps
from kwai.core.db.database import Database
from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.domain.value_objects import InvalidEmailException
from kwai.core.events import Bus
from kwai.core.settings import Settings, SecuritySettings
from kwai.modules.identity import (
    AuthenticateUser,
    AuthenticateUserCommand,
    AuthenticationException,
)
from kwai.modules.identity.recover_user import RecoverUser, RecoverUserCommand
from kwai.modules.identity.refresh_access_token import (
    RefreshAccessTokenCommand,
    RefreshAccessToken,
)
from kwai.modules.identity.tokens.access_token_db_repository import (
    AccessTokenDbRepository,
)
from kwai.modules.identity.tokens.refresh_token import RefreshTokenEntity
from kwai.modules.identity.tokens.refresh_token_db_repository import (
    RefreshTokenDbRepository,
)
from kwai.modules.identity.user_recoveries import UserRecoveryDbRepository
from kwai.modules.identity.users.user_account_db_repository import (
    UserAccountDbRepository,
)
from kwai.modules.identity.users.user_account_repository import (
    UserAccountNotFoundException,
)


class TokenSchema(BaseModel):
    """The schema for an access/refresh token."""

    access_token: str
    refresh_token: str
    expiration: str


router = APIRouter()


@router.post(
    "/login",
    response_model=TokenSchema,
    summary="Create access and refresh token for a user.",
)
async def login(
    settings=deps.depends(Settings),
    db=deps.depends(Database),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """Implements the login API."""
    command = AuthenticateUserCommand(
        username=form_data.username,
        password=form_data.password,
        access_token_expiry_minutes=settings.security.access_token_expires_in,
        refresh_token_expiry_minutes=settings.security.refresh_token_expires_in,
    )

    try:
        refresh_token = AuthenticateUser(
            UserAccountDbRepository(db),
            AccessTokenDbRepository(db),
            RefreshTokenDbRepository(db),
        ).execute(command)
    except InvalidEmailException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email address"
        ) from exc
    except AuthenticationException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)
        ) from exc

    return encode_token(refresh_token, settings.security)


@router.post(
    "/access_token",
    response_model=TokenSchema,
    summary="Renew an access token using a refresh token.",
)
async def renew_access_token(
    settings=deps.depends(Settings),
    db=deps.depends(Database),
    refresh_token: str = Form(),
):
    """Implements the refresh access token API."""
    decoded_refresh_token = jwt.decode(
        refresh_token,
        key=settings.security.jwt_refresh_secret,
        algorithms=[settings.security.jwt_algorithm],
    )

    command = RefreshAccessTokenCommand(
        identifier=decoded_refresh_token["jti"],
        access_token_expiry_minutes=settings.security.access_token_expires_in,
        refresh_token_expiry_minutes=settings.security.refresh_token_expires_in,
    )

    try:
        new_refresh_token = RefreshAccessToken(
            RefreshTokenDbRepository(db), AccessTokenDbRepository(db)
        ).execute(command)
    except AuthenticationException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)
        ) from exc

    return encode_token(new_refresh_token, settings.security)


@router.post(
    "/recover",
    summary="Initiate a password reset flow",
    status_code=status.HTTP_200_OK,
    response_class=Response,
)
async def recover_user(
    email: str = Form(), db=deps.depends(Database), bus=deps.depends(Bus)
) -> None:
    """Initiates a recover password flow for the given email address.

    To avoid leaking information, this api will always respond with 200
    """
    command = RecoverUserCommand(email=email)
    try:
        RecoverUser(
            UserAccountDbRepository(db), UserRecoveryDbRepository(db), bus
        ).execute(command)
    except UserAccountNotFoundException:
        logger.warning(f"Unknown email address used for a password recovery: {email}")
    except UnprocessableException as ex:
        logger.warning(f"User recovery could not be started: {ex}")


class ResetPasswordSchema(BaseModel):
    """Schema for reset password."""

    uuid: str
    password: str


@router.post(
    "/reset",
    response_model=TokenSchema,
    summary="Reset the password of a user.",
)
async def reset_password(db=deps.depends(Database)):
    pass


def encode_token(refresh_token: RefreshTokenEntity, settings: SecuritySettings):
    """Encode the access and refresh token with JWT."""
    return {
        "access_token": jwt.encode(
            {
                "iat": refresh_token.access_token.traceable_time.created_at,
                "exp": refresh_token.access_token.expiration,
                "jti": str(refresh_token.access_token.identifier),
                "sub": str(refresh_token.access_token.user_account.user.uuid),
                "scope": [],
            },
            settings.jwt_secret,
            settings.jwt_algorithm,
        ),
        "refresh_token": jwt.encode(
            {
                "iat": refresh_token.traceable_time.created_at,
                "exp": refresh_token.expiration,
                "jti": str(refresh_token.identifier),
            },
            settings.jwt_refresh_secret,
            settings.jwt_algorithm,
        ),
        "expiration": refresh_token.access_token.expiration.isoformat(" ", "seconds"),
    }
