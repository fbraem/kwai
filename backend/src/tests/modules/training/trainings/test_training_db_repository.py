"""Module for testing the training database repository."""
import pytest

from kwai.core.db.database import Database
from kwai.modules.training.trainings.training import TrainingIdentifier
from kwai.modules.training.trainings.training_db_repository import TrainingDbRepository
from kwai.modules.training.trainings.training_repository import (
    TrainingRepository,
    TrainingNotFoundException,
)

pytestmark = pytest.mark.db


@pytest.fixture(scope="module")
def repo(database: Database) -> TrainingRepository:
    """Fixture for a training repository."""
    return TrainingDbRepository(database)


@pytest.mark.asyncio
async def test_get_all(repo: TrainingRepository):
    """Test get all trainings."""
    trainings = {entity.id: entity async for entity in repo.get_all()}
    assert trainings is not None, "There should be a result"


@pytest.mark.asyncio
async def test_get_by_id(repo: TrainingRepository):
    """Test get training by id."""
    try:
        training = await repo.get_by_id(TrainingIdentifier(1))
        assert training is not None, "There should be a result"
    except TrainingNotFoundException:
        pass
