"""Module that defines the portal api."""
from fastapi import APIRouter

from kwai.api.v1.portal.endpoints import applications

api_router = APIRouter(prefix="/portal")
api_router.include_router(applications.router)
