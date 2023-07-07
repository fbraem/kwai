"""Module that defines the trainings API."""

from fastapi import APIRouter

from kwai.api.v1.trainings.endpoints import trainings

api_router = APIRouter(prefix="/trainings")
api_router.include_router(trainings.router, tags=["trainings"])
