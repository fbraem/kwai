"""Module for testing the use case "Get Training Definitions"."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.training.get_training_definitions import (
    GetTrainingDefinitions,
    GetTrainingDefinitionsCommand,
)
from kwai.modules.training.trainings.training_definition import (
    TrainingDefinitionEntity,
)
from kwai.modules.training.trainings.training_definition_db_repository import (
    TrainingDefinitionDbRepository,
)
from kwai.modules.training.trainings.training_definition_repository import (
    TrainingDefinitionRepository,
)


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
    make_training_definition_in_db,
):
    """Test a successful execution of the use case."""
    definition = await make_training_definition_in_db()
    command = GetTrainingDefinitionsCommand()
    count, iterator = await GetTrainingDefinitions(training_definition_repo).execute(
        command
    )
    assert count >= 1, "There should be at least a training definition"

    definitions = {definition.id: definition async for definition in iterator}
    assert definition.id in definitions, "The definition should be part of the data"
