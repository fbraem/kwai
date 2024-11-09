"""Module for testing the use case "Delete Training"."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.training.delete_training import DeleteTraining, DeleteTrainingCommand
from kwai.modules.training.trainings.training_db_repository import TrainingDbRepository
from kwai.modules.training.trainings.training_repository import (
    TrainingNotFoundException,
    TrainingRepository,
)


@pytest.fixture
def training_repo(database: Database) -> TrainingRepository:
    """A fixture for a training repository."""
    return TrainingDbRepository(database)


async def test_delete_training(training_repo: TrainingRepository, make_training_in_db):
    """Test the use case "Delete Training"."""
    training = await make_training_in_db()
    command = DeleteTrainingCommand(id=training.id.value)
    try:
        await DeleteTraining(training_repo).execute(command)
    except TrainingNotFoundException as ex:
        pytest.fail(str(ex))

    with pytest.raises(TrainingNotFoundException):
        await training_repo.get_by_id(training.id)
