"""Module that defines the trainings API."""

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from kwai.api.dependencies import deps
from kwai.api.v1.trainings.schemas.training import TrainingResource
from kwai.core.db.database import Database
from kwai.core.json_api import Meta, PaginationModel
from kwai.modules.training.get_trainings import GetTrainings, GetTrainingsCommand
from kwai.modules.training.trainings.training_db_repository import TrainingDbRepository

router = APIRouter(tags=["trainings"])


class TrainingsFilterModel(BaseModel):
    """Define the JSON:API filter for trainings."""

    year: int | None = Field(Query(default=None, alias="filter[year]"))
    month: int | None = Field(Query(default=None, alias="filter[month]"))


@router.get("/trainings")
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
    )

    count, training_iterator = await GetTrainings(TrainingDbRepository(db)).execute(
        command
    )

    document = TrainingResource.serialize_list(
        [TrainingResource(training) async for training in training_iterator]
    )
    document.meta = Meta(count=count, offset=command.offset, limit=command.limit)

    return document
