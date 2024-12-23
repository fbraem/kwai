"""Module for testing the use case "Update Training Definition"."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.owner import Owner
from kwai.modules.training.teams.team_db_repository import TeamDbRepository
from kwai.modules.training.teams.team_repository import TeamRepository
from kwai.modules.training.trainings.training_definition_db_repository import (
    TrainingDefinitionDbRepository,
)
from kwai.modules.training.trainings.training_definition_repository import (
    TrainingDefinitionRepository,
)
from kwai.modules.training.update_training_definition import (
    UpdateTrainingDefinition,
    UpdateTrainingDefinitionCommand,
)


@pytest.fixture
def training_definition_repo(database: Database) -> TrainingDefinitionRepository:
    """A fixture for a training repository."""
    return TrainingDefinitionDbRepository(database)


@pytest.fixture
def team_repo(database: Database) -> TeamRepository:
    """A fixture for a team repository."""
    return TeamDbRepository(database)


async def test_update_training_definition(
    training_definition_repo: TrainingDefinitionRepository,
    team_repo: TeamRepository,
    make_training_definition_in_db,
    owner: Owner,
):
    """Test the use case "Update Training"."""
    definition = await make_training_definition_in_db()
    command = UpdateTrainingDefinitionCommand(
        id=definition.id.value,
        name=definition.name,
        description=definition.description,
        weekday=definition.weekday.value,
        start_time="20:00",
        end_time="21:00",
        timezone="Europe/Brussels",
        active=definition.active,
        location=definition.location,
        remark="This is an update test",
        team_id=None,
    )

    training_definition = await UpdateTrainingDefinition(
        training_definition_repo, team_repo, owner
    ).execute(command)

    assert training_definition is not None, "There should be a training definition"
