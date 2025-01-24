"""Module that defines the auth apis."""

from fastapi import APIRouter

from kwai.api.v1.auth.endpoints import login, user, user_invitations, users


api_router = APIRouter(prefix="/auth")
api_router.include_router(login.router, tags=["auth/login"])
api_router.include_router(user.router, tags=["auth/user"])
api_router.include_router(
    user_invitations.router, prefix="/users", tags=["auth/users/invitations"]
)
api_router.include_router(users.router, prefix="/users", tags=["auth/users"])
