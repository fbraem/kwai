"""Module that defines the trainings API."""

from fastapi import APIRouter, Depends

from kwai.api.dependencies import deps
from kwai.api.v1.trainings.schemas.training import TrainingResource
from kwai.core.db.database import Database
from kwai.core.json_api import Meta, PaginationModel
from kwai.modules.training.get_trainings import GetTrainings, GetTrainingsCommand
from kwai.modules.training.trainings.training_db_repository import TrainingDbRepository

router = APIRouter(tags=["trainings"])


@router.get("/")
async def get_trainings(
    pagination: PaginationModel = Depends(PaginationModel),
    db=deps.depends(Database),
) -> TrainingResource.get_document_model():
    """Get all trainings."""
    command = GetTrainingsCommand(offset=pagination.offset or 0, limit=pagination.limit)

    count, training_iterator = await GetTrainings(TrainingDbRepository(db)).execute(
        command
    )

    document = TrainingResource.serialize_list(
        [TrainingResource(training) async for training in training_iterator]
    )
    document.meta = Meta(count=count, offset=command.offset, limit=command.limit)

    return document
