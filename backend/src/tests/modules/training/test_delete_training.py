"""Module for testing the use case "Delete Training"."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.training.delete_training import DeleteTraining, DeleteTrainingCommand
from kwai.modules.training.trainings.training import TrainingEntity
from kwai.modules.training.trainings.training_db_repository import TrainingDbRepository
from kwai.modules.training.trainings.training_repository import (
    TrainingNotFoundException,
    TrainingRepository,
)


@pytest.fixture
def training_repo(database: Database) -> TrainingRepository:
    """A fixture for a training repository."""
    return TrainingDbRepository(database)


@pytest.fixture
async def saved_training_entity(
    training_repo: TrainingRepository, training_entity: TrainingEntity
):
    """A fixture for a training in the repository."""
    return await training_repo.create(training_entity)


async def test_delete_training(
    training_repo: TrainingRepository, saved_training_entity
):
    """Test the use case "Delete Training"."""
    command = DeleteTrainingCommand(id=saved_training_entity.id.value)
    try:
        await DeleteTraining(training_repo).execute(command)
    except TrainingNotFoundException as ex:
        pytest.fail(str(ex))

    with pytest.raises(TrainingNotFoundException):
        await training_repo.get_by_id(saved_training_entity.id)
