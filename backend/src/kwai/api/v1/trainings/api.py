"""Module that defines the trainings API."""

from fastapi import APIRouter

from kwai.api.v1.trainings.endpoints import (
    coaches,
    teams,
    training_definitions,
    trainings,
)

# Remark: Order of include_router is important!
api_router = APIRouter()
api_router.include_router(coaches.router, tags=["training coaches"])
api_router.include_router(teams.router, tags=["training teams"])
api_router.include_router(training_definitions.router, tags=["training definitions"])
api_router.include_router(trainings.router, tags=["trainings"])
