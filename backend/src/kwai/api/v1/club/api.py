"""Module that defines the members API."""

from fastapi import APIRouter

from kwai.api.v1.club.endpoints import members, upload_members

api_router = APIRouter(prefix="/club")
api_router.include_router(upload_members.router, tags=["club"])
api_router.include_router(members.router, tags=["club"])
