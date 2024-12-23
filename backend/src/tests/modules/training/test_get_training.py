"""Module for testing the use case "Get Training"."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.training.get_training import GetTraining, GetTrainingCommand
from kwai.modules.training.trainings.training_db_repository import TrainingDbRepository
from kwai.modules.training.trainings.training_repository import (
    TrainingRepository,
)


@pytest.fixture
def training_repo(database: Database) -> TrainingRepository:
    """A fixture for a training repository."""
    return TrainingDbRepository(database)


async def test_get_training(training_repo: TrainingRepository, make_training_in_db):
    """Test the use case "Get Training"."""
    training = await make_training_in_db()
    command = GetTrainingCommand(id=training.id.value)
    training = await GetTraining(training_repo).execute(command)
    assert training is not None, "There should be a training."
