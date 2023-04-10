"""Module that defines the auth apis."""
from fastapi import APIRouter

from kwai.api.v1.auth.endpoints import login, user, user_invitations

api_router = APIRouter(prefix="/auth")
api_router.include_router(login.router)
api_router.include_router(user.router)
api_router.include_router(user_invitations.router, prefix="/users")
