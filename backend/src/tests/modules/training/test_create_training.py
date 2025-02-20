"""Module for testing the use case "Create Training"."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.use_case import TextCommand
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.modules.training.coaches.coach import CoachEntity
from kwai.modules.training.coaches.coach_db_repository import CoachDbRepository
from kwai.modules.training.coaches.coach_repository import CoachRepository
from kwai.modules.training.create_training import CreateTraining, CreateTrainingCommand
from kwai.modules.training.teams.team_db_repository import TeamDbRepository
from kwai.modules.training.teams.team_repository import TeamRepository
from kwai.modules.training.training_command import Coach
from kwai.modules.training.trainings.training_db_repository import TrainingDbRepository
from kwai.modules.training.trainings.training_definition_db_repository import (
    TrainingDefinitionDbRepository,
)
from kwai.modules.training.trainings.training_definition_repository import (
    TrainingDefinitionRepository,
)
from kwai.modules.training.trainings.training_repository import TrainingRepository


@pytest.fixture
def training_repo(database: Database) -> TrainingRepository:
    """A fixture for a training repository."""
    return TrainingDbRepository(database)


@pytest.fixture
def coach_repo(database: Database) -> CoachRepository:
    """A fixture for a coach repository."""
    return CoachDbRepository(database)


@pytest.fixture
def definition_repo(database: Database) -> TrainingDefinitionRepository:
    """A fixture for a training definition repository."""
    return TrainingDefinitionDbRepository(database)


@pytest.fixture
def team_repo(database: Database) -> TeamRepository:
    """A fixture for a team repository."""
    return TeamDbRepository(database)


@pytest.fixture
async def coach(make_coach_in_db) -> CoachEntity:
    """A fixture for a coach."""
    return await make_coach_in_db()


@pytest.fixture
async def command(make_coach_in_db, make_team_in_db) -> CreateTrainingCommand:
    """A fixture for a training entity."""
    coach = await make_coach_in_db()
    team = await make_team_in_db()
    start_date = Timestamp.create_now()
    return CreateTrainingCommand(
        start_date=str(start_date),
        end_date=str(start_date.add_delta(hours=1)),
        active=True,
        cancelled=False,
        location="",
        texts=[
            TextCommand(
                locale="en",
                format="md",
                title="Test training",
                content="This is a test",
                summary="This is a test",
            )
        ],
        coaches=[Coach(id=coach.id.value, head=True, present=False, payed=False)],
        teams=[team.id.value],
        definition=None,
        remark="Created with test_create_training",
    )


async def test_create_training(
    command: CreateTrainingCommand,
    training_repo: TrainingRepository,
    definition_repo: TrainingDefinitionRepository,
    coach_repo: CoachRepository,
    team_repo: TeamRepository,
    owner: Owner,
):
    """Test the use case "Create Training"."""
    training = await CreateTraining(
        training_repo, definition_repo, coach_repo, team_repo, owner
    ).execute(command)

    assert training is not None, "There should be a training"
