"""Module for testing the training definition repository."""

import pytest
from kwai.core.db.database import Database
from kwai.core.domain.entity import Entity
from kwai.modules.training.trainings.training_definition import (
    TrainingDefinitionEntity,
)
from kwai.modules.training.trainings.training_definition_db_repository import (
    TrainingDefinitionDbRepository,
)
from kwai.modules.training.trainings.training_definition_repository import (
    TrainingDefinitionNotFoundException,
    TrainingDefinitionRepository,
)

pytestmark = pytest.mark.db


@pytest.fixture(scope="module")
def repo(database: Database) -> TrainingDefinitionRepository:
    """Fixture for a training definition repository."""
    return TrainingDefinitionDbRepository(database)


@pytest.fixture
async def saved_training_definition(
    repo: TrainingDefinitionRepository,
    training_definition: TrainingDefinitionEntity,
) -> TrainingDefinitionEntity:
    """A fixture for a training definition in the database."""
    return await repo.create(training_definition)


def test_create(saved_training_definition: TrainingDefinitionEntity):
    """Test if the training definition was created."""
    assert (
        not saved_training_definition.id.is_empty()
    ), "There should be a training definition created"


async def test_get_by_id(
    repo: TrainingDefinitionRepository,
    saved_training_definition: TrainingDefinitionEntity,
):
    """Test if the training definition can be found with the id."""
    entity = await repo.get_by_id(saved_training_definition.id)

    assert (
        entity.id == saved_training_definition.id
    ), "The training definition should be found"


async def test_get_all(repo: TrainingDefinitionRepository):
    """Test if all training definitions can be loaded."""
    entities = {entity.id: entity async for entity in repo.get_all()}
    assert entities is not None, "There should be a result"


async def test_update(
    repo: TrainingDefinitionRepository,
    saved_training_definition: TrainingDefinitionEntity,
):
    """Test update of training definition."""
    training_definition = Entity.replace(
        saved_training_definition, remark="Training definition updated"
    )
    await repo.update(training_definition)


async def test_delete(
    repo: TrainingDefinitionRepository,
    saved_training_definition: TrainingDefinitionEntity,
):
    """Test if the training definition can be deleted."""
    await repo.delete(saved_training_definition)

    with pytest.raises(TrainingDefinitionNotFoundException):
        await repo.get_by_id(saved_training_definition.id)
