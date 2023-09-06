"""Module for endpoints for training definitions."""
from fastapi import APIRouter, Depends, HTTPException, status

from kwai.api.dependencies import deps, get_current_user
from kwai.api.v1.trainings.schemas.training_definition import TrainingDefinitionResource
from kwai.core.db.database import Database
from kwai.core.json_api import Meta, PaginationModel
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.training.get_training_definition import (
    GetTrainingDefinition,
    GetTrainingDefinitionCommand,
)
from kwai.modules.training.get_training_definitions import (
    GetTrainingDefinitions,
    GetTrainingDefinitionsCommand,
)
from kwai.modules.training.trainings.training_definition_db_repository import (
    TrainingDefinitionDbRepository,
)
from kwai.modules.training.trainings.training_definition_repository import (
    TrainingDefinitionNotFoundException,
)

router = APIRouter()


@router.get("/training_definitions")
async def get_training_definitions(
    pagination: PaginationModel = Depends(PaginationModel), db=deps.depends(Database)
) -> TrainingDefinitionResource.get_document_model():
    """Get all training definitions."""
    command = GetTrainingDefinitionsCommand(
        offset=pagination.offset or 0, limit=pagination.limit
    )
    count, iterator = await GetTrainingDefinitions(
        TrainingDefinitionDbRepository(db)
    ).execute(command)
    document = TrainingDefinitionResource.serialize_list(
        [
            TrainingDefinitionResource(training_definition)
            async for training_definition in iterator
        ]
    )
    document.meta = Meta(count=count, offset=command.offset, limit=command.limit)
    return document


@router.get(
    "/training_definitions/{training_definition_id",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Training definition was not found."}
    },
)
async def get_training_definition(
    training_definition_id: int,
    db=deps.depends(Database),
) -> TrainingDefinitionResource.get_document_model():
    """Get training definition with the given id."""
    command = GetTrainingDefinitionCommand(id=training_definition_id)
    try:
        training_definition = await GetTrainingDefinition(
            TrainingDefinitionDbRepository(db)
        ).execute(command)
    except TrainingDefinitionNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex

    return TrainingDefinitionResource.serialize(
        TrainingDefinitionResource(training_definition)
    )


@router.post(
    "/training_definitions",
    status_code=status.HTTP_201_CREATED,
)
async def create_training_definition(
    resource: TrainingDefinitionResource.get_resource_data_model(),
    db=deps.depends(Database),
    user: UserEntity = Depends(get_current_user),
) -> TrainingDefinitionResource.get_document_model():
    """Create a new training definition."""


@router.patch(
    "/training_definitions/{training_definition_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Training definition was not found."}
    },
)
async def update_training_definition(
    training_definition_id: int,
    resource: TrainingDefinitionResource.get_resource_data_model(),
    db=deps.depends(Database),
    user: UserEntity = Depends(get_current_user),
) -> TrainingDefinitionResource.get_document_model():
    """Update a training definition."""


@router.delete(
    "/training_definitions/{training_definition_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Training definition was not found."}
    },
)
async def delete_training_definition(
    training_definition_id: int,
    resource: TrainingDefinitionResource.get_resource_data_model(),
    db=deps.depends(Database),
    user: UserEntity = Depends(get_current_user),
) -> None:
    """Delete a training definition."""
