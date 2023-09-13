"""Module for testing the use case "Get Training Definitions"."""
from typing import AsyncIterator

import pytest

from kwai.core.db.database import Database
from kwai.modules.training.get_training_definitions import (
    GetTrainingDefinitions,
    GetTrainingDefinitionsCommand,
)
from kwai.modules.training.trainings.training_definition import (
    TrainingDefinitionEntity,
    TrainingDefinitionIdentifier,
)
from kwai.modules.training.trainings.training_definition_db_repository import (
    TrainingDefinitionDbRepository,
)
from kwai.modules.training.trainings.training_definition_repository import (
    TrainingDefinitionRepository,
)


async def _find(iterator: AsyncIterator, id_: TrainingDefinitionIdentifier):
    """Search for an entity with the given id."""
    async for entity in iterator:
        if entity.id == id_:
            return entity
    return None


@pytest.fixture(scope="module")
def training_definition_repo(database: Database) -> TrainingDefinitionRepository:
    """A fixture for a training definition repository."""
    return TrainingDefinitionDbRepository(database)


@pytest.fixture
async def saved_training_definition(
    training_definition_repo: TrainingDefinitionRepository,
    training_definition: TrainingDefinitionEntity,
) -> TrainingDefinitionEntity:
    """A fixture for a training definition in the database."""
    return await training_definition_repo.create(training_definition)


async def test_get_training_definitions(
    training_definition_repo: TrainingDefinitionRepository,
    saved_training_definition: TrainingDefinitionEntity,
):
    """Test a successful execution of the use case."""
    command = GetTrainingDefinitionsCommand()
    count, iterator = await GetTrainingDefinitions(training_definition_repo).execute(
        command
    )
    assert count >= 1, "There should be at least a training definition"

    entity = await _find(iterator, saved_training_definition.id)
    assert entity is not None, "The definition should be part of the data"
