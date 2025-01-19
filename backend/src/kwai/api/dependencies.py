"""Module that integrates the dependencies in FastAPI."""

from typing import Annotated, AsyncGenerator

import jwt

from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from faststream.redis import RedisBroker
from faststream.security import SASLPlaintext
from jwt import ExpiredSignatureError

from kwai.core.db.database import Database
from kwai.core.events.fast_stream_publisher import FastStreamPublisher
from kwai.core.events.publisher import Publisher
from kwai.core.settings import SecuritySettings, Settings, get_settings
from kwai.core.template.jinja2_engine import Jinja2Engine
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


async def create_templates(settings=Depends(get_settings)) -> Jinja2Templates:
    """Create the template engine dependency."""
    return Jinja2Engine(website=settings.website).web_templates


async def get_current_user(
    settings: Annotated[Settings, Depends(get_settings)],
    db: Annotated[Database, Depends(create_database)],
    access_token: Annotated[str, Cookie()],
) -> UserEntity:
    """Try to get the current user from the access token.

    Not authorized will be raised when the access token is not found, expired, revoked
    or when the user is revoked.
    """
    return await _get_user_from_token(access_token, settings.security, db)


optional_oauth = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


async def get_publisher(
    settings=Depends(get_settings),
) -> AsyncGenerator[Publisher, None]:
    """Get the publisher dependency."""
    broker = RedisBroker(
        url=f"redis://{settings.redis.host}:{settings.redis.port}",
        # middlewares=[LoggerMiddleware],
        security=SASLPlaintext(
            username="",
            password=settings.redis.password,
        ),
    )
    await broker.start()
    yield FastStreamPublisher(broker)


async def get_optional_user(
    settings: Annotated[Settings, Depends(get_settings)],
    db: Annotated[Database, Depends(create_database)],
    access_token: Annotated[str | None, Cookie()] = None,
) -> UserEntity | None:
    """Try to get the current user from an access token.

    When no token is available in the request, None will be returned.

    Not authorized will be raised when the access token is expired, revoked
    or when the user is revoked.
    """
    if access_token is None:
        return None

    return await _get_user_from_token(access_token, settings.security, db)


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
