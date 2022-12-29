"""Module for defining the security dependency."""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from kwai.core.db.database import get_database
from kwai.core.security.system_user import SystemUser
from kwai.core.settings import get_settings
from kwai.modules.identity.tokens import (
    AccessTokenDbRepository,
    AccessTokenNotFoundException,
    TokenIdentifier,
)

oauth = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    settings=Depends(get_settings),
    db=Depends(get_database),
    token: str = Depends(oauth),
) -> SystemUser:
    """Try to get the current user from the access token.

    Not authorized will be raised when the access token is not found, expired, revoked
    or when the user is revoked.
    """
    payload = jwt.decode(
        token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
    )
    access_token_repo = AccessTokenDbRepository(db)
    try:
        access_token = access_token_repo.get_by_identifier(
            TokenIdentifier(payload["jti"])
        )
    except AccessTokenNotFoundException as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    # Check if the access token is assigned to the user we have in the subject of JWT.
    if not access_token().user_account().user.uuid == payload["sub"]:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if access_token().revoked:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if access_token().user_account().revoked:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if access_token().is_expired:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return SystemUser(
        id=access_token().user_account.id, uuid=access_token().user_account().user.uuid
    )
