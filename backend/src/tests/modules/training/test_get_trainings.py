"""Module for testing the use case "Get Trainings"."""

import pytest
from kwai.core.db.database import Database
from kwai.core.domain.value_objects.period import Period
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.modules.training.coaches.coach_db_repository import CoachDbRepository
from kwai.modules.training.coaches.coach_repository import CoachRepository
from kwai.modules.training.get_trainings import GetTrainings, GetTrainingsCommand
from kwai.modules.training.trainings.training_db_repository import TrainingDbRepository
from kwai.modules.training.trainings.training_definition_db_repository import (
    TrainingDefinitionDbRepository,
)
from kwai.modules.training.trainings.training_definition_repository import (
    TrainingDefinitionRepository,
)
from kwai.modules.training.trainings.training_repository import TrainingRepository


@pytest.fixture
def training_repo(database: Database) -> TrainingRepository:
    """A fixture for a training repository."""
    return TrainingDbRepository(database)


@pytest.fixture
def coach_repo(database: Database) -> CoachRepository:
    """A fixture for a coach repository."""
    return CoachDbRepository(database)


@pytest.fixture
def definition_repo(database: Database) -> TrainingDefinitionRepository:
    """A fixture for a training definition repository."""
    return TrainingDefinitionDbRepository(database)


async def test_get_active_trainings(
    training_repo: TrainingRepository,
    coach_repo: CoachRepository,
    definition_repo: TrainingDefinitionRepository,
    make_training_in_db,
):
    """Test the use case "Get Trainings"."""
    training = await make_training_in_db()
    command = GetTrainingsCommand(active=True)
    count, iterator = await GetTrainings(
        training_repo, coach_repo, definition_repo
    ).execute(command)
    assert count > 0, "There should be at least one active training"

    entities = {entity.id: entity async for entity in iterator}
    assert training.id in entities, "The training should be returned"


async def test_get_year_month_trainings(
    training_repo: TrainingRepository,
    coach_repo: CoachRepository,
    definition_repo: TrainingDefinitionRepository,
    make_training_in_db,
    make_training,
):
    """Test the use case "Get Trainings"."""
    start_date = Timestamp.create_from_string("2024-01-01 19:00:00")
    training = await make_training_in_db(
        make_training(period=Period.create_from_delta(start_date, hours=2))
    )
    command = GetTrainingsCommand(limit=10, year=2024, month=1)
    count, iterator = await GetTrainings(
        training_repo, coach_repo, definition_repo
    ).execute(command)
    assert count > 0, "There should be at least one training in 01/2023."
    entities = {entity.id: entity async for entity in iterator}
    assert training.id in entities, "The training should be returned in the result."
