"""Module that implements all APIs for login."""
from fastapi import APIRouter, Depends, status, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from lagom.integrations.fast_api import FastApiIntegration
from pydantic import BaseModel

from kwai.core.db.database import get_database, Database
from kwai.core.dependencies import container
from kwai.core.domain.value_objects import InvalidEmailException
from kwai.core.settings import Settings
from kwai.modules.identity import (
    AuthenticateUser,
    AuthenticateUserCommand,
    AuthenticationException,
)
from kwai.modules.identity.refresh_access_token import (
    RefreshAccessTokenCommand,
    RefreshAccessToken,
)
from kwai.modules.identity.tokens import (
    AccessTokenDbRepository,
    RefreshTokenDbRepository,
    RefreshTokenEntity,
)
from kwai.modules.identity.users import UserAccountDbRepository

deps = FastApiIntegration(container)


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

    return encode_token(refresh_token, settings)


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

    return encode_token(new_refresh_token, settings)


class ResetPasswordSchema(BaseModel):
    """Schema for reset password."""

    uuid: str
    password: str


@router.post(
    "/reset",
    response_model=TokenSchema,
    summary="Reset the password of a user.",
)
async def reset_password(db=Depends(get_database)):
    pass


def encode_token(refresh_token: RefreshTokenEntity, settings: Settings):
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
            settings.security.jwt_secret,
            settings.security.jwt_algorithm,
        ),
        "refresh_token": jwt.encode(
            {
                "iat": refresh_token.traceable_time.created_at,
                "exp": refresh_token.expiration,
                "jti": str(refresh_token.identifier),
            },
            settings.security.jwt_refresh_secret,
            settings.security.jwt_algorithm,
        ),
        "expiration": refresh_token.access_token.expiration.isoformat(" ", "seconds"),
    }
