"""Module for testing the training database repository."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.period import Period
from kwai.core.domain.value_objects.text import LocaleText
from kwai.modules.training.coaches.coach import CoachEntity, CoachIdentifier
from kwai.modules.training.trainings.training import TrainingEntity, TrainingIdentifier
from kwai.modules.training.trainings.training_db_repository import TrainingDbRepository
from kwai.modules.training.trainings.training_repository import (
    TrainingNotFoundException,
    TrainingRepository,
)
from kwai.modules.training.trainings.value_objects import TrainingCoach

pytestmark = pytest.mark.db


@pytest.fixture(scope="module")
def repo(database: Database) -> TrainingRepository:
    """Fixture for a training repository."""
    return TrainingDbRepository(database)


@pytest.fixture(scope="module")
def training(user, context) -> TrainingEntity:
    """A fixture for a training."""
    coach = context["coaches"][0]
    person = context["persons"][0]

    text = [
        LocaleText(
            locale="en",
            format="md",
            title="Training U13",
            summary="Training for U13",
            content="",
            author=Owner(id=user.id, uuid=user.uuid, name=user.name),
        )
    ]
    return TrainingEntity(
        content=text,
        period=Period.create_from_delta(hours=1),
        coaches=[
            TrainingCoach(
                coach=CoachEntity(
                    id_=CoachIdentifier(coach.id),
                    name=Name(first_name=person.firstname, last_name=person.lastname),
                    active=True,
                ),
                owner=Owner(id=user.id, uuid=user.uuid, name=user.name),
                remark="Test Training Coach",
            )
        ],
    )


@pytest.mark.asyncio
async def test_create(repo: TrainingRepository, training: TrainingEntity):
    """Test create a training."""
    new_training = await repo.create(training)
    assert new_training is not None, "There should be a training."


@pytest.mark.asyncio
async def test_get_all(repo: TrainingRepository):
    """Test get all trainings."""
    trainings = {entity.id: entity async for entity in repo.get_all()}
    assert trainings is not None, "There should be a result"


@pytest.mark.asyncio
async def test_get_by_id(repo: TrainingRepository):
    """Test get training by id."""
    try:
        training = await repo.get_by_id(TrainingIdentifier(1))
        assert training is not None, "There should be a result"
    except TrainingNotFoundException:
        pass
