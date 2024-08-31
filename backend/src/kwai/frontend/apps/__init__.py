"""Package for defining the routes for all frontend applications."""

from fastapi import APIRouter

from kwai.frontend.apps._auth import router as auth_router
from kwai.frontend.apps._author import router as author_router
from kwai.frontend.apps._club import router as club_router
from kwai.frontend.apps._coach import router as coach_router
from kwai.frontend.apps._portal import router as portal_router

# All routers, except for the portal, because that will be added as root by the frontend
# application.
apps_router = APIRouter()
apps_router.include_router(auth_router)
apps_router.include_router(author_router)
apps_router.include_router(club_router)
apps_router.include_router(coach_router)
apps_router.include_router(portal_router)
