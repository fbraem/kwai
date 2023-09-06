"""Module that defines the trainings API."""

from fastapi import APIRouter

from kwai.api.v1.trainings.endpoints import training_definitions, trainings

api_router = APIRouter()
api_router.include_router(trainings.router, tags=["trainings"])
api_router.include_router(training_definitions.router, tags=["training definitions"])
