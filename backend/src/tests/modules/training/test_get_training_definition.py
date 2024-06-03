"""Module for testing the use case "Get Training Definition"."""

import pytest
from kwai.core.db.database import Database
from kwai.modules.training.get_training_definition import (
    GetTrainingDefinition,
    GetTrainingDefinitionCommand,
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


async def test_get_training_definition(
    training_definition_repo: TrainingDefinitionRepository,
    make_training_definition_in_db,
):
    """Test a successful execution of the use case."""
    definition = await make_training_definition_in_db()
    command = GetTrainingDefinitionCommand(id=definition.id.value)
    training_definition = await GetTrainingDefinition(training_definition_repo).execute(
        command
    )
    assert training_definition is not None, "There should be a training definition"
