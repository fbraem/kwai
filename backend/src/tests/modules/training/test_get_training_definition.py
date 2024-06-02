"""Module for testing the use case "Get Training Definition"."""

import pytest
from kwai.core.db.database import Database
from kwai.modules.training.get_training_definition import (
    GetTrainingDefinition,
    GetTrainingDefinitionCommand,
)
from kwai.modules.training.trainings.training_definition import TrainingDefinitionEntity
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


async def test_get_training_definition(
    training_definition_repo: TrainingDefinitionRepository,
    saved_training_definition: TrainingDefinitionEntity,
):
    """Test a successful execution of the use case."""
    command = GetTrainingDefinitionCommand(id=saved_training_definition.id.value)
    training_definition = await GetTrainingDefinition(training_definition_repo).execute(
        command
    )
    assert training_definition is not None, "There should be a training definition"
