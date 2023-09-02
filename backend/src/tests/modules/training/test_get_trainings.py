"""Module for testing the use case "Get Trainings"."""
import pytest

from kwai.core.db.database import Database
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
):
    """Test the use case "Get Trainings"."""
    command = GetTrainingsCommand(active=True, limit=10)
    count, iterator = await GetTrainings(
        training_repo, coach_repo, definition_repo
    ).execute(command)
    entities = {entity.id: entity async for entity in iterator}

    assert entities is not None, "There should be a result"


async def test_get_year_month_trainings(
    training_repo: TrainingRepository,
    coach_repo: CoachRepository,
    definition_repo: TrainingDefinitionRepository,
):
    """Test the use case "Get Trainings"."""
    command = GetTrainingsCommand(limit=10, year=2023, month=1)
    count, iterator = await GetTrainings(
        training_repo, coach_repo, definition_repo
    ).execute(command)
    entities = {entity.id: entity async for entity in iterator}

    assert entities is not None, "There should be a result"
