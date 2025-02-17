"""Module that defines endpoints for SSO logins."""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.params import Depends
from fastapi.responses import RedirectResponse
from fastapi_sso import GoogleSSO

from kwai.api.dependencies import create_database
from kwai.api.v1.auth.cookies import create_cookies
from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.core.settings import Settings, get_settings
from kwai.modules.identity.authenticate_user import (
    AuthenticateUser,
    AuthenticateUserCommand,
)
from kwai.modules.identity.tokens.access_token_db_repository import (
    AccessTokenDbRepository,
)
from kwai.modules.identity.tokens.refresh_token_db_repository import (
    RefreshTokenDbRepository,
)
from kwai.modules.identity.users.user_account_db_repository import (
    UserAccountDbRepository,
)
from kwai.modules.identity.users.user_account_repository import (
    UserAccountNotFoundException,
)


router = APIRouter()


async def get_google_sso(
    settings: Annotated[Settings, Depends(get_settings)],
) -> GoogleSSO:
    """Google SSO dependency."""
    if settings.security.google is None:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Google SSO is not configured",
        )

    return GoogleSSO(
        settings.security.google.client_id,
        settings.security.google.client_secret,
        redirect_uri=f"{settings.website.url}/api/v1/auth/sso/google/callback",
        allow_insecure_http=settings.frontend.test,
    )


@router.get("/google/login")
async def google_login(
    google_sso: Annotated[GoogleSSO, Depends(get_google_sso)],
    return_url: str | None = None,
):
    """Initiate the Google login process."""
    async with google_sso:
        return await google_sso.get_login_redirect(state=return_url)


@router.get("/google/callback")
async def google_callback(
    request: Request,
    google_sso: Annotated[GoogleSSO, Depends(get_google_sso)],
    db: Annotated[Database, Depends(create_database)],
    settings: Annotated[Settings, Depends(get_settings)],
    state: str | None = None,
):
    """Implement the Google login callback."""
    async with google_sso:
        openid = await google_sso.verify_and_process(request)
        if not openid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
            )

    async with UnitOfWork(db):
        try:
            refresh_token = await AuthenticateUser(
                UserAccountDbRepository(db),
                AccessTokenDbRepository(db),
                RefreshTokenDbRepository(db),
            ).execute(AuthenticateUserCommand(username=str(openid.email)))
        except UserAccountNotFoundException as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown user account"
            ) from exc

    if state is not None:
        response = RedirectResponse(state)
    else:
        response = RedirectResponse(settings.website.url)

    create_cookies(response, refresh_token, settings)

    return response
