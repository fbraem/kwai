"""Module for endpoints for trainings."""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from kwai.api.dependencies import create_database, get_current_user
from kwai.api.v1.trainings.schemas.training import TrainingDocument
from kwai.core.domain.use_case import TextCommand
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.json_api import Meta, PaginationModel
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.training.coaches.coach_db_repository import CoachDbRepository
from kwai.modules.training.coaches.coach_repository import CoachNotFoundException
from kwai.modules.training.create_training import (
    CreateTraining,
    CreateTrainingCommand,
)
from kwai.modules.training.delete_training import DeleteTraining, DeleteTrainingCommand
from kwai.modules.training.get_training import GetTraining, GetTrainingCommand
from kwai.modules.training.get_trainings import GetTrainings, GetTrainingsCommand
from kwai.modules.training.teams.team_db_repository import TeamDbRepository
from kwai.modules.training.training_command import Coach
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
from kwai.modules.training.update_training import UpdateTraining, UpdateTrainingCommand

router = APIRouter()


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
    db=Depends(create_database),
) -> TrainingDocument:
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

    document: TrainingDocument = TrainingDocument(
        meta=Meta(count=count, offset=command.offset, limit=command.limit), data=[]
    )
    async for training in training_iterator:
        document.merge(TrainingDocument.create(training))

    return document


@router.get(
    "/trainings/{training_id}",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Training was not found."}},
)
async def get_training(
    training_id: int,
    db=Depends(create_database),
) -> TrainingDocument:
    """Get the training with the given id."""
    command = GetTrainingCommand(id=training_id)

    try:
        training = await GetTraining(TrainingDbRepository(db)).execute(command)
    except TrainingNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex

    return TrainingDocument.create(training)


@router.post(
    "/trainings",
    status_code=status.HTTP_201_CREATED,
)
async def create_training(
    resource: TrainingDocument,
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
) -> TrainingDocument:
    """Create a new training."""
    command = CreateTrainingCommand(
        start_date=resource.data.attributes.event.start_date,
        end_date=resource.data.attributes.event.end_date,
        active=resource.data.attributes.event.active,
        cancelled=resource.data.attributes.event.cancelled,
        texts=[
            TextCommand(
                locale=text.locale,
                format=text.format,
                title=text.title,
                summary=text.original_summary,
                content=text.original_content,
            )
            for text in resource.data.attributes.texts
        ],
        coaches=[
            Coach(
                id=int(coach.id),
                head=coach.head,
                present=coach.present,
                payed=coach.payed,
            )
            for coach in resource.data.attributes.coaches
        ],
        teams=[int(team.id) for team in resource.data.relationships.teams.data],
        definition=None
        if resource.data.relationships.definition.data is None
        else resource.data.relationships.definition.data.id,
        location=resource.data.attributes.event.location,
        remark=resource.data.attributes.remark,
    )

    try:
        training = await CreateTraining(
            TrainingDbRepository(db),
            TrainingDefinitionDbRepository(db),
            CoachDbRepository(db),
            TeamDbRepository(db),
            Owner(id=user.id, uuid=user.uuid, name=user.name),
        ).execute(command)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve)
        ) from ve

    return TrainingDocument.create(training)


@router.patch(
    "/trainings/{training_id}",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Training was not found."}},
)
async def update_training(
    training_id: int,
    resource: TrainingDocument,
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
) -> TrainingDocument:
    """Update a training."""
    command = UpdateTrainingCommand(
        id=training_id,
        start_date=resource.data.attributes.event.start_date,
        end_date=resource.data.attributes.event.end_date,
        active=resource.data.attributes.event.active,
        cancelled=resource.data.attributes.event.cancelled,
        texts=[
            TextCommand(
                locale=text.locale,
                format=text.format,
                title=text.title,
                summary=text.original_summary,
                content=text.original_content,
            )
            for text in resource.data.attributes.texts
        ],
        coaches=[
            Coach(
                id=int(coach.id),
                head=coach.head,
                present=coach.present,
                payed=coach.payed,
            )
            for coach in resource.data.attributes.coaches
        ],
        teams=[int(team.id) for team in resource.data.relationships.teams.data],
        definition=None
        if resource.data.relationships.definition.data is None
        else resource.data.relationships.definition.data.id,
        location=resource.data.attributes.event.location,
        remark=resource.data.attributes.remark,
    )

    try:
        training = await UpdateTraining(
            TrainingDbRepository(db),
            TrainingDefinitionDbRepository(db),
            CoachDbRepository(db),
            TeamDbRepository(db),
            Owner(id=user.id, uuid=user.uuid, name=user.name),
        ).execute(command)
    except TrainingNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve)
        ) from ve

    return TrainingDocument.create(training)


@router.delete(
    "/trainings/{training_id}",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Training was not found."}},
)
async def delete_training(
    training_id: int,
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
) -> None:
    """Delete a training definition."""
    command = DeleteTrainingCommand(id=training_id)
    await DeleteTraining(TrainingDbRepository(db)).execute(command)
