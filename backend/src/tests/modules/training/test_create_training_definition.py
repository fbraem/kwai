"""Module for testing the use case "Create Training Definition"."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.owner import Owner
from kwai.modules.training.create_training_definition import (
    CreateTrainingDefinition,
    CreateTrainingDefinitionCommand,
)
from kwai.modules.training.teams.team_db_repository import TeamDbRepository
from kwai.modules.training.teams.team_repository import TeamRepository
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
def team_repo(database: Database) -> TeamRepository:
    """A fixture for a team repository."""
    return TeamDbRepository(database)


@pytest.fixture
async def command(make_team_in_db):
    """A fixture for a create command."""
    team = await make_team_in_db()
    return CreateTrainingDefinitionCommand(
        name="U11 Monday Training",
        description="Training for U11 on Monday",
        weekday=1,
        start_time="20:00",
        end_time="21:00",
        timezone="Europe/Brussels",
        active=True,
        location="Sports Hall",
        remark="Test",
        team_id=team.id.value,
    )


async def test_create_training_definition(
    training_definition_repo: TrainingDefinitionRepository,
    team_repo: TeamRepository,
    command: CreateTrainingDefinitionCommand,
    owner: Owner,
):
    """Test the use "Create Training Definition"."""
    training_definition = await CreateTrainingDefinition(
        training_definition_repo, team_repo, owner
    ).execute(command)
    assert training_definition is not None, "There should be a training definition."
