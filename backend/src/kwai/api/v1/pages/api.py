"""Module for defining the pages API."""

from fastapi import APIRouter

from kwai.api.v1.pages.endpoints import pages


api_router = APIRouter()
api_router.include_router(pages.router, tags=["pages"])
