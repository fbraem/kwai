"""Module for testing the training definition repository."""

import pytest
from kwai.core.db.database import Database
from kwai.core.db.exceptions import QueryException
from kwai.core.domain.entity import Entity
from kwai.modules.training.trainings.training_definition_db_repository import (
    TrainingDefinitionDbRepository,
)
from kwai.modules.training.trainings.training_definition_repository import (
    TrainingDefinitionNotFoundException,
)

pytestmark = pytest.mark.db


async def test_create(make_training_definition_in_db):
    """Test if the training definition was created."""
    definition = await make_training_definition_in_db()
    assert definition is not None, "There should be a training definition created"


async def test_get_by_id(
    database: Database,
    make_training_definition_in_db,
):
    """Test if the training definition can be found with the id."""
    repo = TrainingDefinitionDbRepository(database)
    definition = await make_training_definition_in_db()
    entity = await repo.get_by_id(definition.id)

    assert entity.id == definition.id, "The training definition should be found"


async def test_get_all(
    database: Database,
    make_training_definition_in_db,
):
    """Test if all training definitions can be loaded."""
    repo = TrainingDefinitionDbRepository(database)
    definition = await make_training_definition_in_db()
    entities = {entity.id: entity async for entity in repo.get_all()}
    assert definition.id in entities, "Definition should be in the list."


async def test_update(
    database: Database,
    make_training_definition_in_db,
):
    """Test update of training definition."""
    repo = TrainingDefinitionDbRepository(database)
    definition = await make_training_definition_in_db()
    definition = Entity.replace(definition, remark="Training definition updated")
    try:
        await repo.update(definition)
    except QueryException as qe:
        pytest.fail(str(qe))


async def test_delete(
    database: Database,
    make_training_definition_in_db,
):
    """Test if the training definition can be deleted."""
    repo = TrainingDefinitionDbRepository(database)
    definition = await make_training_definition_in_db()
    await repo.delete(definition)

    with pytest.raises(TrainingDefinitionNotFoundException):
        await repo.get_by_id(definition.id)
