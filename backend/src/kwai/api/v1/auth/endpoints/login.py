"""Module that implements all APIs for login."""

from typing import Annotated

import jwt

from fastapi import APIRouter, Cookie, Depends, Form, HTTPException, status
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger

from kwai.api.dependencies import create_database, get_publisher
from kwai.api.v1.auth.cookies import create_cookies, delete_cookies
from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.domain.value_objects.email_address import InvalidEmailException
from kwai.core.events.publisher import Publisher
from kwai.core.settings import Settings, get_settings
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
from kwai.modules.identity.users.user_account_db_repository import (
    UserAccountDbRepository,
)
from kwai.modules.identity.users.user_account_repository import (
    UserAccountNotFoundException,
)


router = APIRouter()


@router.post(
    "/login",
    summary="Create access and refresh token for a user.",
    responses={
        200: {"description": "The user is logged in successfully."},
        401: {
            "description": "The email is invalid, authentication failed or user is unknown."
        },
    },
)
async def login(
    settings: Annotated[Settings, Depends(get_settings)],
    db: Annotated[Database, Depends(create_database)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
):
    """Login a user.

    This request expects a form (application/x-www-form-urlencoded). The form
    must contain a `username` and `password` field. The username is
    the email address of the user.

    On success, a cookie for the access token and the refresh token will be returned.
    """
    command = AuthenticateUserCommand(
        username=form_data.username,
        password=form_data.password,
        access_token_expiry_minutes=settings.security.access_token_expires_in,
        refresh_token_expiry_minutes=settings.security.refresh_token_expires_in,
    )

    try:
        async with UnitOfWork(db):
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

    create_cookies(response, refresh_token, settings)
    response.status_code = status.HTTP_200_OK

    return response


@router.post(
    "/logout",
    summary="Logout the current user",
    responses={
        200: {"description": "The user is logged out successfully."},
        404: {"description": "The token is not found."},
    },
)
async def logout(
    settings: Annotated[Settings, Depends(get_settings)],
    db: Annotated[Database, Depends(create_database)],
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
) -> None:
    """Log out the current user.

    A user is logged out by revoking the refresh token. The associated access token
    will also be revoked.

    This request expects a form (application/x-www-form-urlencoded). The form
    must contain a **refresh_token** field.
    """
    if refresh_token:
        decoded_refresh_token = jwt.decode(
            refresh_token,
            key=settings.security.jwt_refresh_secret,
            algorithms=[settings.security.jwt_algorithm],
        )
        command = LogoutCommand(identifier=decoded_refresh_token["jti"])
        try:
            async with UnitOfWork(db):
                await Logout(
                    refresh_token_repository=RefreshTokenDbRepository(db),
                    access_token_repository=AccessTokenDbRepository(db),
                ).execute(command)
        except RefreshTokenNotFoundException as ex:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
            ) from ex

    delete_cookies(response)
    response.status_code = status.HTTP_200_OK


@router.post(
    "/access_token",
    summary="Renew an access token using a refresh token.",
    responses={
        200: {"description": "The access token is renewed."},
        401: {"description": "The refresh token is expired."},
    },
)
async def renew_access_token(
    settings: Annotated[Settings, Depends(get_settings)],
    db: Annotated[Database, Depends(create_database)],
    refresh_token: Annotated[str, Cookie()],
    response: Response,
):
    """Refresh the access token.

    On success, a new access token / refresh token cookie will be sent.

    When the refresh token is expired, the user needs to log in again.
    """
    try:
        decoded_refresh_token = jwt.decode(
            refresh_token,
            key=settings.security.jwt_refresh_secret,
            algorithms=[settings.security.jwt_algorithm],
        )
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)
        ) from exc

    command = RefreshAccessTokenCommand(
        identifier=decoded_refresh_token["jti"],
        access_token_expiry_minutes=settings.security.access_token_expires_in,
        refresh_token_expiry_minutes=settings.security.refresh_token_expires_in,
    )

    try:
        async with UnitOfWork(db):
            new_refresh_token = await RefreshAccessToken(
                RefreshTokenDbRepository(db), AccessTokenDbRepository(db)
            ).execute(command)
    except AuthenticationException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)
        ) from exc

    create_cookies(response, new_refresh_token, settings)
    response.status_code = status.HTTP_200_OK


@router.post(
    "/recover",
    summary="Initiate a password reset flow",
    responses={
        200: {"description": "Ok."},
    },
)
async def recover_user(
    db: Annotated[Database, Depends(create_database)],
    publisher: Annotated[Publisher, Depends(get_publisher)],
    email: Annotated[str, Form()],
) -> None:
    """Start a recover password flow for the given email address.

    A mail with a unique id will be sent using the message bus.

    This request expects a form (application/x-www-form-urlencoded). The form
    must contain an **email** field.

    !!! Note
        To avoid leaking information, this api will always respond with 200
    """
    command = RecoverUserCommand(email=email)
    try:
        async with UnitOfWork(db):
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
    responses={  # noqa B006
        200: {"description": "The password is reset successfully."},
        403: {"description": "This request is forbidden."},
        404: {"description": "The uniqued id of the recovery could not be found."},
        422: {"description": "The user could not be found."},
    },
)
async def reset_password(
    uuid: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: Annotated[Database, Depends(create_database)],
):
    """Reset the password of the user.

    Http code 200 on success, 404 when the unique id is invalid, 422 when the
    request can't be processed, 403 when the request is forbidden.

    This request expects a form (application/x-www-form-urlencoded). The form
    must contain an **uuid** and **password** field. The unique id must be valid
    and is retrieved by [/api/v1/auth/recover][post_/recover].
    """
    command = ResetPasswordCommand(uuid=uuid, password=password)
    try:
        async with UnitOfWork(db):
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
