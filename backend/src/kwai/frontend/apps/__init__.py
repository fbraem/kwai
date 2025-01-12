"""Package for defining the routes for all frontend applications."""

from kwai.frontend.apps._auth import router as auth_router
from kwai.frontend.apps._author import router as author_router
from kwai.frontend.apps._club import router as club_router
from kwai.frontend.apps._coach import router as coach_router
from kwai.frontend.apps._portal import router as portal_router


application_routers = [
    auth_router,
    author_router,
    club_router,
    coach_router,
    portal_router,
]
