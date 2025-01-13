"""Module for testing the training database repository."""

import pytest

from kwai.core.db.database import Database
from kwai.core.db.exceptions import QueryException
from kwai.core.domain.entity import Entity
from kwai.modules.training.trainings.training_db_repository import TrainingDbRepository
from kwai.modules.training.trainings.training_repository import (
    TrainingRepository,
)


pytestmark = pytest.mark.db


@pytest.fixture(scope="module")
def repo(database: Database) -> TrainingRepository:
    """Fixture for a training repository."""
    return TrainingDbRepository(database)


async def test_create(make_training_in_db):
    """Test create a training."""
    training = await make_training_in_db()
    assert training is not None, "There should be a training."


async def test_update(repo: TrainingRepository, make_training_in_db):
    """Test update of a training."""
    training = await make_training_in_db()
    updated_training = Entity.replace(training, remark="This training is updated.")
    try:
        await repo.update(updated_training)
    except QueryException as qe:
        pytest.fail(str(qe))


async def test_get_all(repo: TrainingRepository, make_training_in_db):
    """Test get all trainings."""
    training = await make_training_in_db()
    trainings = {entity.id: entity async for entity in repo.get_all()}
    assert training.id in trainings, "The training should be returned in the list"


async def test_get_by_id(repo: TrainingRepository, make_training_in_db):
    """Test get training by id."""
    training = await make_training_in_db()
    training = await repo.get_by_id(training.id)
    assert training is not None, "There should be a result"


async def test_delete(repo: TrainingRepository, make_training_in_db):
    """Test delete of a training."""
    training = await make_training_in_db()
    try:
        await repo.delete(training)
    except QueryException as qe:
        pytest.fail(str(qe))


async def test_reset_definition(database: Database, make_training_definition_in_db):
    """Test reset definition."""
    definition = await make_training_definition_in_db()
    repo = TrainingDbRepository(database)
    await repo.reset_definition(definition, False)
