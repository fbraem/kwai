"""Module for endpoints for training definitions."""
from fastapi import APIRouter, Depends, HTTPException, status

from kwai.api.dependencies import get_current_user
from kwai.api.v1.trainings.endpoints.trainings import TrainingsFilterModel
from kwai.api.v1.trainings.schemas.training import TrainingDocument
from kwai.api.v1.trainings.schemas.training_definition import (
    TrainingDefinitionDocument,
)
from kwai.core.dependencies import create_database
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.json_api import Meta, PaginationModel
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.training.coaches.coach_db_repository import CoachDbRepository
from kwai.modules.training.coaches.coach_repository import CoachNotFoundException
from kwai.modules.training.create_training_definition import (
    CreateTrainingDefinition,
    CreateTrainingDefinitionCommand,
)
from kwai.modules.training.delete_training_definition import (
    DeleteTrainingDefinition,
    DeleteTrainingDefinitionCommand,
)
from kwai.modules.training.get_training_definition import (
    GetTrainingDefinition,
    GetTrainingDefinitionCommand,
)
from kwai.modules.training.get_training_definitions import (
    GetTrainingDefinitions,
    GetTrainingDefinitionsCommand,
)
from kwai.modules.training.get_trainings import GetTrainings, GetTrainingsCommand
from kwai.modules.training.teams.team_db_repository import TeamDbRepository
from kwai.modules.training.trainings.training_db_repository import TrainingDbRepository
from kwai.modules.training.trainings.training_definition_db_repository import (
    TrainingDefinitionDbRepository,
)
from kwai.modules.training.trainings.training_definition_repository import (
    TrainingDefinitionNotFoundException,
)
from kwai.modules.training.update_training_definition import (
    UpdateTrainingDefinition,
    UpdateTrainingDefinitionCommand,
)

router = APIRouter()


@router.get("/training_definitions")
async def get_training_definitions(
    pagination: PaginationModel = Depends(PaginationModel),
    db=Depends(create_database),
) -> TrainingDefinitionDocument:
    """Get all training definitions."""
    command = GetTrainingDefinitionsCommand(
        offset=pagination.offset or 0, limit=pagination.limit
    )
    count, iterator = await GetTrainingDefinitions(
        TrainingDefinitionDbRepository(db)
    ).execute(command)

    document: TrainingDefinitionDocument = TrainingDefinitionDocument(
        meta=Meta(count=count, offset=command.offset, limit=command.limit), data=[]
    )
    async for training_definition in iterator:
        document.merge(TrainingDefinitionDocument.create(training_definition))

    return document


@router.get(
    "/training_definitions/{training_definition_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Training definition was not found."}
    },
)
async def get_training_definition(
    training_definition_id: int,
    db=Depends(create_database),
) -> TrainingDefinitionDocument:
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

    return TrainingDefinitionDocument.create(training_definition)


@router.post(
    "/training_definitions",
    status_code=status.HTTP_201_CREATED,
)
async def create_training_definition(
    resource: TrainingDefinitionDocument,
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
) -> TrainingDefinitionDocument:
    """Create a new training definition."""
    if (
        resource.data.relationships is not None
        and resource.data.relationships.team is not None
        and resource.data.relationships.team.data is not None
    ):
        team_id = int(resource.data.relationships.team.data.id)
    else:
        team_id = None

    command = CreateTrainingDefinitionCommand(
        name=resource.data.attributes.name,
        description=resource.data.attributes.description,
        weekday=resource.data.attributes.weekday,
        start_time=resource.data.attributes.start_time,
        end_time=resource.data.attributes.end_time,
        active=resource.data.attributes.active,
        location=resource.data.attributes.location or "",
        remark=resource.data.attributes.remark or "",
        team_id=team_id,
    )
    try:
        training_definition = await CreateTrainingDefinition(
            TrainingDefinitionDbRepository(db),
            TeamDbRepository(db),
            Owner(id=user.id, uuid=user.uuid, name=user.name),
        ).execute(command)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve)
        ) from ve

    return TrainingDefinitionDocument.create(training_definition)


@router.patch(
    "/training_definitions/{training_definition_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Training definition was not found."}
    },
)
async def update_training_definition(
    training_definition_id: int,
    resource: TrainingDefinitionDocument,
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
) -> TrainingDefinitionDocument:
    """Update a training definition."""
    if (
        resource.data.relationships is not None
        and resource.data.relationships.team is not None
        and resource.data.relationships.team.data is not None
    ):
        team_id = int(resource.data.relationships.team.data.id)
    else:
        team_id = None
    command = UpdateTrainingDefinitionCommand(
        id=training_definition_id,
        name=resource.data.attributes.name,
        description=resource.data.attributes.description,
        weekday=resource.data.attributes.weekday,
        start_time=resource.data.attributes.start_time,
        end_time=resource.data.attributes.end_time,
        active=resource.data.attributes.active,
        location=resource.data.attributes.location or "",
        remark=resource.data.attributes.remark or "",
        team_id=team_id,
    )
    try:
        training_definition = await UpdateTrainingDefinition(
            TrainingDefinitionDbRepository(db),
            TeamDbRepository(db),
            Owner(id=user.id, uuid=user.uuid, name=user.name),
        ).execute(command)
    except TrainingDefinitionNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve)
        ) from ve

    return TrainingDefinitionDocument.create(training_definition)


@router.delete(
    "/training_definitions/{training_definition_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Training definition was not found."}
    },
)
async def delete_training_definition(
    training_definition_id: int,
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
) -> None:
    """Delete a training definition."""
    command = DeleteTrainingDefinitionCommand(
        id=training_definition_id, delete_trainings=False
    )
    await DeleteTrainingDefinition(
        TrainingDefinitionDbRepository(db), TrainingDbRepository(db)
    ).execute(command)


@router.get(
    "/training_definitions/{training_definition_id}/trainings",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Training definition or coach was not found."
        }
    },
)
async def get_trainings(
    training_definition_id: int,
    pagination: PaginationModel = Depends(PaginationModel),
    trainings_filter: TrainingsFilterModel = Depends(TrainingsFilterModel),
    db=Depends(create_database),
) -> TrainingDocument:
    """Get trainings of the given training definition."""
    command = GetTrainingsCommand(
        offset=pagination.offset or 0,
        limit=pagination.limit,
        year=trainings_filter.year,
        month=trainings_filter.month,
        start=trainings_filter.start,
        end=trainings_filter.end,
        active=trainings_filter.active,
        coach=trainings_filter.coach,
        definition=training_definition_id,
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

    document: TrainingDocument = TrainingDocument(
        meta=Meta(count=count, offset=command.offset, limit=command.limit), data=[]
    )
    async for training in training_iterator:
        document.merge(TrainingDocument.create(training))

    return document
