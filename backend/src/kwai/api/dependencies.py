"""Module that integrates the dependencies in FastAPI."""
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from lagom.integrations.fast_api import FastApiIntegration

from kwai.core.db.database import Database
from kwai.core.dependencies import container
from kwai.core.security.system_user import SystemUser
from kwai.core.settings import Settings
from kwai.modules.identity.tokens.access_token_db_repository import (
    AccessTokenDbRepository,
)
from kwai.modules.identity.tokens.access_token_repository import (
    AccessTokenNotFoundException,
)
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier

deps = FastApiIntegration(container)

oauth = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    settings=deps.depends(Settings),
    db=deps.depends(Database),
    token: str = Depends(oauth),
) -> SystemUser:
    """Try to get the current user from the access token.

    Not authorized will be raised when the access token is not found, expired, revoked
    or when the user is revoked.
    """
    payload = jwt.decode(
        token,
        settings.security.jwt_secret,
        algorithms=[settings.security.jwt_algorithm],
    )
    access_token_repo = AccessTokenDbRepository(db)
    try:
        access_token = access_token_repo.get_by_identifier(
            TokenIdentifier(bytes=payload["jti"])
        )
    except AccessTokenNotFoundException as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED) from exc

    # Check if the access token is assigned to the user we have in the subject of JWT.
    if not access_token.user_account.user.uuid == payload["sub"]:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if access_token.revoked:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if access_token.user_account.revoked:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if access_token.expired:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return SystemUser(
        id=access_token.user_account.id.value, uuid=access_token.user_account.user.uuid
    )
