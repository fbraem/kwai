"""Module that integrates the dependencies in FastAPI."""
from typing import AsyncGenerator

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from faststream.rabbit import RabbitBroker
from jwt import ExpiredSignatureError

from kwai.core.db.database import Database
from kwai.core.events.faststream_publisher import FaststreamPublisher
from kwai.core.events.publisher import Publisher
from kwai.core.settings import SecuritySettings, get_settings
from kwai.modules.identity.tokens.access_token_db_repository import (
    AccessTokenDbRepository,
)
from kwai.modules.identity.tokens.access_token_repository import (
    AccessTokenNotFoundException,
)
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.users.user import UserEntity

oauth = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def create_database(
    settings=Depends(get_settings),
) -> AsyncGenerator[Database, None]:
    """Create the database dependency."""
    database = Database(settings.db)
    try:
        yield database
    finally:
        await database.close()


async def get_current_user(
    settings=Depends(get_settings),
    db=Depends(create_database),
    token: str = Depends(oauth),
) -> UserEntity:
    """Try to get the current user from the access token.

    Not authorized will be raised when the access token is not found, expired, revoked
    or when the user is revoked.
    """
    return await _get_user_from_token(token, settings.security, db)


optional_oauth = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def get_publisher(settings=Depends(get_settings)) -> Publisher:
    """Get the publisher dependency."""
    return FaststreamPublisher(
        RabbitBroker(
            host=settings.rabbitmq.host,
            port=settings.rabbitmq.port,
            login=settings.rabbitmq.user,
            password=settings.rabbitmq.password,
            virtualhost=settings.rabbitmq.vhost,
        )
    )


async def get_optional_user(
    settings=Depends(get_settings),
    db=Depends(create_database),
    token: str = Depends(optional_oauth),
) -> UserEntity | None:
    """Try to get the current user from an access token.

    When no token is available in the request, None will be returned.

    Not authorized will be raised when the access token is expired, revoked
    or when the user is revoked.
    """
    if token is None:
        return None

    return await _get_user_from_token(token, settings.security, db)


async def _get_user_from_token(
    token: str, security_settings: SecuritySettings, db: Database
) -> UserEntity:
    """Try to get the user from the token.

    Returns: The user associated with the access token.
    """
    try:
        payload = jwt.decode(
            token,
            security_settings.jwt_secret,
            algorithms=[security_settings.jwt_algorithm],
        )
    except ExpiredSignatureError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    access_token_repo = AccessTokenDbRepository(db)
    try:
        access_token = await access_token_repo.get_by_identifier(
            TokenIdentifier(hex_string=payload["jti"])
        )
    except AccessTokenNotFoundException as exc:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="The access token is unknown."
        ) from exc

    # Check if the access token is assigned to the user we have in the subject of JWT.
    if not access_token.user_account.user.uuid == payload["sub"]:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if access_token.revoked:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if access_token.user_account.revoked:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if access_token.expired:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return access_token.user_account.user
