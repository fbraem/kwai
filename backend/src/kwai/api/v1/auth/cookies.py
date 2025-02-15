"""Module that defines methods for handling cookies."""

import jwt

from starlette.responses import Response

from kwai.core.settings import Settings
from kwai.modules.identity.tokens.refresh_token import RefreshTokenEntity


COOKIE_ACCESS_TOKEN = "access_token"
COOKIE_REFRESH_TOKEN = "refresh_token"
COOKIE_KWAI = "kwai"


def delete_cookies(response: Response):
    """Delete all cookies."""
    response.delete_cookie(key=COOKIE_KWAI)
    response.delete_cookie(key=COOKIE_ACCESS_TOKEN)
    response.delete_cookie(key=COOKIE_REFRESH_TOKEN)


def create_cookies(
    response: Response, refresh_token: RefreshTokenEntity, settings: Settings
) -> None:
    """Create cookies for access en refresh token."""
    encoded_access_token = jwt.encode(
        {
            "iat": refresh_token.access_token.traceable_time.created_at.timestamp,
            "exp": refresh_token.access_token.expiration.timestamp,
            "jti": str(refresh_token.access_token.identifier),
            "sub": str(refresh_token.access_token.user_account.user.uuid),
            "scope": [],
        },
        settings.security.jwt_secret,
        settings.security.jwt_algorithm,
    )
    encoded_refresh_token = jwt.encode(
        {
            "iat": refresh_token.traceable_time.created_at.timestamp,
            "exp": refresh_token.expiration.timestamp,
            "jti": str(refresh_token.identifier),
        },
        settings.security.jwt_refresh_secret,
        settings.security.jwt_algorithm,
    )
    response.set_cookie(
        key=COOKIE_KWAI,
        value="Y",
        expires=refresh_token.expiration.timestamp,
        secure=settings.frontend.test,
    )
    response.set_cookie(
        key=COOKIE_ACCESS_TOKEN,
        value=encoded_access_token,
        expires=refresh_token.access_token.expiration.timestamp,
        httponly=True,
        secure=not settings.frontend.test,
    )
    response.set_cookie(
        key=COOKIE_REFRESH_TOKEN,
        value=encoded_refresh_token,
        expires=refresh_token.expiration.timestamp,
        httponly=True,
        secure=not settings.frontend.test,
    )
