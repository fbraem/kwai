"""Module that implements all APIs for login."""

import jwt
from fastapi import APIRouter, Depends, Form, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from jwt import ExpiredSignatureError
from loguru import logger
from pydantic import BaseModel

from kwai.api.dependencies import get_current_user, get_publisher
from kwai.core.db.database import Database
from kwai.core.dependencies import create_database
from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.domain.value_objects.email_address import InvalidEmailException
from kwai.core.events.publisher import Publisher
from kwai.core.settings import SecuritySettings, Settings, get_settings
from kwai.modules.identity.authenticate_user import (
    AuthenticateUser,
    AuthenticateUserCommand,
    AuthenticationException,
)
from kwai.modules.identity.exceptions import NotAllowedException
from kwai.modules.identity.logout import Logout, LogoutCommand
from kwai.modules.identity.recover_user import RecoverUser, RecoverUserCommand
from kwai.modules.identity.refresh_access_token import (
    RefreshAccessToken,
    RefreshAccessTokenCommand,
)
from kwai.modules.identity.reset_password import ResetPassword, ResetPasswordCommand
from kwai.modules.identity.tokens.access_token_db_repository import (
    AccessTokenDbRepository,
)
from kwai.modules.identity.tokens.refresh_token import RefreshTokenEntity
from kwai.modules.identity.tokens.refresh_token_db_repository import (
    RefreshTokenDbRepository,
)
from kwai.modules.identity.tokens.refresh_token_repository import (
    RefreshTokenNotFoundException,
)
from kwai.modules.identity.user_recoveries.user_recovery_db_repository import (
    UserRecoveryDbRepository,
)
from kwai.modules.identity.user_recoveries.user_recovery_repository import (
    UserRecoveryNotFoundException,
)
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.identity.users.user_account_db_repository import (
    UserAccountDbRepository,
)
from kwai.modules.identity.users.user_account_repository import (
    UserAccountNotFoundException,
)


class TokenSchema(BaseModel):
    """The response schema for an access/refresh token.

    Attributes:
        access_token:
        refresh_token:
        expiration: Timestamp in format YYYY-MM-DD HH:MM:SS
    """

    access_token: str
    refresh_token: str
    expiration: str


router = APIRouter()


@router.post(
    "/login",
    summary="Create access and refresh token for a user.",
)
async def login(
    settings: Settings = Depends(get_settings),
    db: Database = Depends(create_database),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> TokenSchema:
    """Login a user.

    The response is a TokenSchema.

    Note:
        This request expects a form (application/x-www-form-urlencoded).

    Args:
        settings: Settings dependency
        db: Database dependency
        form_data: Form data that contains the username and password
    """
    command = AuthenticateUserCommand(
        username=form_data.username,
        password=form_data.password,
        access_token_expiry_minutes=settings.security.access_token_expires_in,
        refresh_token_expiry_minutes=settings.security.refresh_token_expires_in,
    )

    try:
        refresh_token = await AuthenticateUser(
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
    except UserAccountNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)
        ) from exc

    return _encode_token(refresh_token, settings.security)


@router.post("/logout", summary="Logout the current user")
async def logout(
    settings=Depends(get_settings),
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
    refresh_token: str = Form(),
):
    """Log out the current user.

    A user is logged out by revoking the refresh token. The associated access token
    will also be revoked.

    Args:
        settings: Settings dependency
        db: Database dependency
        user: The currently logged-in user
        refresh_token: The active refresh token of the user

    Returns:
        Http code 200 on success, 401 when the user is not logged in,
        404 when the refresh token is not found.
    """
    decoded_refresh_token = jwt.decode(
        refresh_token,
        key=settings.security.jwt_refresh_secret,
        algorithms=[settings.security.jwt_algorithm],
    )
    command = LogoutCommand(identifier=decoded_refresh_token["jti"])
    try:
        await Logout(
            refresh_token_repository=RefreshTokenDbRepository(db),
            access_token_repository=AccessTokenDbRepository(db),
        ).execute(command)
    except RefreshTokenNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex


@router.post(
    "/access_token",
    summary="Renew an access token using a refresh token.",
)
async def renew_access_token(
    settings=Depends(get_settings),
    db=Depends(create_database),
    refresh_token: str = Form(),
) -> TokenSchema:
    """Refresh the access token.

    Args:
        settings(Settings): Settings dependency
        db(Database): Database dependency
        refresh_token(str): The active refresh token of the user

    Returns:
        TokenSchema: On success a new TokenSchema is returned.
    """
    try:
        decoded_refresh_token = jwt.decode(
            refresh_token,
            key=settings.security.jwt_refresh_secret,
            algorithms=[settings.security.jwt_algorithm],
        )
    except ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)
        ) from exc

    command = RefreshAccessTokenCommand(
        identifier=decoded_refresh_token["jti"],
        access_token_expiry_minutes=settings.security.access_token_expires_in,
        refresh_token_expiry_minutes=settings.security.refresh_token_expires_in,
    )

    try:
        new_refresh_token = await RefreshAccessToken(
            RefreshTokenDbRepository(db), AccessTokenDbRepository(db)
        ).execute(command)
    except AuthenticationException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)
        ) from exc

    return _encode_token(new_refresh_token, settings.security)


@router.post(
    "/recover",
    summary="Initiate a password reset flow",
    status_code=status.HTTP_200_OK,
    response_class=Response,
)
async def recover_user(
    email: str = Form(),
    db=Depends(create_database),
    publisher: Publisher = Depends(get_publisher),
) -> None:
    """Start a recover password flow for the given email address.

    A mail with a unique id will be sent using the message bus.

    Note:
        To avoid leaking information, this api will always respond with 200

    Args:
        email(str): The email of the user that wants to reset the password.
        db(Database): Database dependency
        publisher(Publisher): A publisher to publish the event
    """
    command = RecoverUserCommand(email=email)
    try:
        await RecoverUser(
            UserAccountDbRepository(db), UserRecoveryDbRepository(db), publisher
        ).execute(command)
    except UserAccountNotFoundException:
        logger.warning(f"Unknown email address used for a password recovery: {email}")
    except UnprocessableException as ex:
        logger.warning(f"User recovery could not be started: {ex}")


@router.post(
    "/reset",
    summary="Reset the password of a user.",
    status_code=status.HTTP_200_OK,
)
async def reset_password(uuid=Form(), password=Form(), db=Depends(create_database)):
    """Reset the password of the user.

    Args:
        uuid(str): The unique id of the password recovery.
        password(str): The new password
        db(Database): Database dependency

    Returns:
        Http code 200 on success, 404 when the unique is invalid, 422 when the
        request can't be processed, 403 when the request is forbidden.
    """
    command = ResetPasswordCommand(uuid=uuid, password=password)
    try:
        await ResetPassword(
            user_account_repo=UserAccountDbRepository(db),
            user_recovery_repo=UserRecoveryDbRepository(db),
        ).execute(command)
    except UserRecoveryNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from exc
    except UserAccountNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY) from exc
    except NotAllowedException as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from exc


def _encode_token(
    refresh_token: RefreshTokenEntity, settings: SecuritySettings
) -> TokenSchema:
    """Encode the access and refresh token with JWT.

    Args:
        refresh_token: The refresh token entity.
        settings: The security settings.

    Returns:
        A dictionary with the access token, refresh token and expiration timestamp.
    """
    return TokenSchema(
        access_token=jwt.encode(
            {
                "iat": refresh_token.access_token.traceable_time.created_at.timestamp,
                "exp": refresh_token.access_token.expiration,
                "jti": str(refresh_token.access_token.identifier),
                "sub": str(refresh_token.access_token.user_account.user.uuid),
                "scope": [],
            },
            settings.jwt_secret,
            settings.jwt_algorithm,
        ),
        refresh_token=jwt.encode(
            {
                "iat": refresh_token.traceable_time.created_at.timestamp,
                "exp": refresh_token.expiration,
                "jti": str(refresh_token.identifier),
            },
            settings.jwt_refresh_secret,
            settings.jwt_algorithm,
        ),
        expiration=refresh_token.access_token.expiration.isoformat(" ", "seconds"),
    )
