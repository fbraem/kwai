"""Module that defines the portal api."""

from fastapi import APIRouter

from kwai.api.v1.news.endpoints import news


api_router = APIRouter()
api_router.include_router(news.router, tags=["news"])
