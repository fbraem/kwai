"""Module for testing the use case "Update Training Definition"."""

import pytest
from kwai.core.db.database import Database
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.time_period import TimePeriod
from kwai.core.domain.value_objects.weekday import Weekday
from kwai.modules.training.teams.team_db_repository import TeamDbRepository
from kwai.modules.training.teams.team_repository import TeamRepository
from kwai.modules.training.trainings.training_definition import TrainingDefinitionEntity
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


@pytest.fixture
async def training_definition_entity(
    training_definition_repo: TrainingDefinitionRepository,
    owner: Owner,
) -> TrainingDefinitionEntity:
    """A fixture for a training definition entity."""
    return await training_definition_repo.create(
        TrainingDefinitionEntity(
            name="U9 Training",
            description="Test Training Definition",
            weekday=Weekday.MONDAY,
            period=TimePeriod.create_from_string("19:00", "20:00"),
            owner=owner,
        )
    )


async def test_update_training_definition(
    training_definition_entity: TrainingDefinitionEntity,
    training_definition_repo: TrainingDefinitionRepository,
    team_repo: TeamRepository,
    owner: Owner,
):
    """Test the use case "Update Training"."""
    command = UpdateTrainingDefinitionCommand(
        id=training_definition_entity.id.value,
        name=training_definition_entity.name,
        description=training_definition_entity.description,
        weekday=training_definition_entity.weekday.value,
        start_time="20:00",
        end_time="21:00",
        timezone="Europe/Brussels",
        active=training_definition_entity.active,
        location=training_definition_entity.location,
        remark="This is an update test",
        team_id=None,
    )

    training_definition = await UpdateTrainingDefinition(
        training_definition_repo, team_repo, owner
    ).execute(command)

    assert training_definition is not None, "There should be a training definition"
