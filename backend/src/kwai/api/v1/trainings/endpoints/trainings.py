"""Module that defines the trainings API."""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from kwai.api.dependencies import deps
from kwai.api.v1.trainings.schemas.training import TrainingResource
from kwai.core.db.database import Database
from kwai.core.json_api import Meta, PaginationModel
from kwai.modules.training.coaches.coach_db_repository import CoachDbRepository
from kwai.modules.training.coaches.coach_repository import CoachNotFoundException
from kwai.modules.training.get_training import GetTraining, GetTrainingCommand
from kwai.modules.training.get_trainings import GetTrainings, GetTrainingsCommand
from kwai.modules.training.trainings.training_db_repository import TrainingDbRepository
from kwai.modules.training.trainings.training_definition_db_repository import (
    TrainingDefinitionDbRepository,
)
from kwai.modules.training.trainings.training_definition_repository import (
    TrainingDefinitionNotFoundException,
)
from kwai.modules.training.trainings.training_repository import (
    TrainingNotFoundException,
)

router = APIRouter(tags=["trainings"])


class TrainingsFilterModel(BaseModel):
    """Define the JSON:API filter for trainings."""

    year: int | None = Field(Query(default=None, alias="filter[year]"))
    month: int | None = Field(Query(default=None, alias="filter[month]"))
    start: datetime | None = Field(Query(default=None, alias="filter[start]"))
    end: datetime | None = Field(Query(default=None, alias="filter[end]"))
    active: bool = Field(Query(default=True, alias="filter[active]"))
    coach: int | None = Field(Query(default=None, alias="filter[coach]"))
    definition: int | None = Field(Query(default=None, alias="filter[definition]"))


@router.get(
    "/trainings",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Coach or Training definition was not found."
        }
    },
)
async def get_trainings(
    pagination: PaginationModel = Depends(PaginationModel),
    trainings_filter: TrainingsFilterModel = Depends(TrainingsFilterModel),
    db=deps.depends(Database),
) -> TrainingResource.get_document_model():
    """Get all trainings."""
    command = GetTrainingsCommand(
        offset=pagination.offset or 0,
        limit=pagination.limit,
        year=trainings_filter.year,
        month=trainings_filter.month,
        start=trainings_filter.start,
        end=trainings_filter.end,
        active=trainings_filter.active,
        coach=trainings_filter.coach,
        definition=trainings_filter.definition,
    )

    try:
        count, training_iterator = await GetTrainings(
            TrainingDbRepository(db),
            CoachDbRepository(db),
            TrainingDefinitionDbRepository(db),
        ).execute(command)
    except TrainingDefinitionNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex
    except CoachNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex

    document = TrainingResource.serialize_list(
        [TrainingResource(training) async for training in training_iterator]
    )
    document.meta = Meta(count=count, offset=command.offset, limit=command.limit)

    return document


@router.get(
    "/trainings/{training_id}",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Training was not found."}},
)
async def get_training(
    training_id: int,
    db=deps.depends(Database),
) -> TrainingResource.get_document_model():
    """Get the training with the given id."""
    command = GetTrainingCommand(id=training_id)

    try:
        training = await GetTraining(TrainingDbRepository(db)).execute(command)
    except TrainingNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex

    return TrainingResource.serialize(TrainingResource(training))
