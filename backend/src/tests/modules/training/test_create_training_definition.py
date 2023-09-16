"""Module for testing the use case "Create Training Definition"."""
import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.owner import Owner
from kwai.modules.training.create_training_definition import (
    CreateTrainingDefinition,
    CreateTrainingDefinitionCommand,
)
from kwai.modules.training.trainings.training_definition_db_repository import (
    TrainingDefinitionDbRepository,
)
from kwai.modules.training.trainings.training_definition_repository import (
    TrainingDefinitionRepository,
)


@pytest.fixture
def training_definition_repo(database: Database) -> TrainingDefinitionRepository:
    """A fixture for a training definition repository."""
    return TrainingDefinitionDbRepository(database)


@pytest.fixture
def command():
    """A fixture for a create command."""
    return CreateTrainingDefinitionCommand(
        name="U11 Monday Training",
        description="Training for U11 on Monday",
        weekday=1,
        start_time="20:00",
        end_time="21:00",
        active=True,
        location="Sports Hall",
        remark="Test",
    )


async def test_create_training_definition(
    training_definition_repo: TrainingDefinitionRepository,
    command: CreateTrainingDefinitionCommand,
    owner: Owner,
):
    """Test the use "Create Training Definition"."""
    training_definition = await CreateTrainingDefinition(
        training_definition_repo, owner
    ).execute(command)
    assert training_definition is not None, "There should be a training definition."
