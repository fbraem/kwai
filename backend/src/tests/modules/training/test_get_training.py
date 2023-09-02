"""Module for testing the use case "Get Training"."""
import pytest

from kwai.core.db.database import Database
from kwai.modules.training.get_training import GetTraining, GetTrainingCommand
from kwai.modules.training.trainings.training_db_repository import TrainingDbRepository
from kwai.modules.training.trainings.training_repository import (
    TrainingNotFoundException,
    TrainingRepository,
)


@pytest.fixture
def training_repo(database: Database) -> TrainingRepository:
    """A fixture for a training repository."""
    return TrainingDbRepository(database)


async def test_get_training(training_repo: TrainingRepository):
    """Test the use case "Get Training"."""
    command = GetTrainingCommand(id=1)
    try:
        training = await GetTraining(training_repo).execute(command)
        assert training is not None, "There should be a training."
    except TrainingNotFoundException:
        pass
