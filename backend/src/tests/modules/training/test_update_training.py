"""Module for testing the use case "Update Training"."""

import pytest
from kwai.core.db.database import Database
from kwai.core.domain.use_case import TextCommand
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.modules.training.coaches.coach_db_repository import CoachDbRepository
from kwai.modules.training.coaches.coach_repository import CoachRepository
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
from kwai.modules.training.update_training import UpdateTraining, UpdateTrainingCommand


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


async def test_update_training(
    training_repo: TrainingRepository,
    definition_repo: TrainingDefinitionRepository,
    coach_repo: CoachRepository,
    team_repo: TeamRepository,
    make_training_in_db,
    owner: Owner,
):
    """Test the use case "Update Training"."""
    training = await make_training_in_db()
    start_date = Timestamp.create_now().add_delta(hours=1)
    end_date = start_date.add_delta(hours=1)
    command = UpdateTrainingCommand(
        id=training.id.value,
        start_date=str(start_date),
        end_date=str(end_date),
        active=training.active,
        cancelled=training.cancelled,
        location=training.location,
        texts=[
            TextCommand(
                locale="en",
                format="md",
                title="Updated Test Training",
                content="This is a test (updated)",
                summary="This is a test (updated)",
            )
        ],
        remark="This is a test",
        coaches=[
            Coach(
                id=training.coaches[0].coach.id.value,
                head=training_coach.type == 1,
                present=training_coach.present,
                payed=training_coach.payed,
            )
            for training_coach in training.coaches
        ],
        teams=[team.id.value for team in training.teams],
        definition=None,
    )

    training = await UpdateTraining(
        training_repo, definition_repo, coach_repo, team_repo, owner
    ).execute(command)

    assert training is not None, "There should be a training"
    assert training.texts[0].title == "Updated Test Training"
