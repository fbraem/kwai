"""Module for testing the training definition repository."""

import datetime

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.time_period import TimePeriod
from kwai.core.domain.value_objects.weekday import Weekday
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.training.trainings.training_definition import (
    TrainingDefinitionEntity,
)
from kwai.modules.training.trainings.training_definition_db_repository import (
    TrainingDefinitionDbRepository,
)
from kwai.modules.training.trainings.training_definition_repository import (
    TrainingDefinitionNotFoundException,
    TrainingDefinitionRepository,
)

pytestmark = pytest.mark.db


def _find(entity_list: list, id_: IntIdentifier):
    """Search for an entity with the given id."""
    for entity in entity_list:
        if entity.id == id_:
            return entity
    return None


@pytest.fixture(scope="module")
def repo(database: Database) -> TrainingDefinitionRepository:
    """Fixture for a training definition repository."""
    return TrainingDefinitionDbRepository(database)


@pytest.fixture(scope="module")
async def training_definition(
    repo: TrainingDefinitionRepository, user: UserEntity
) -> TrainingDefinitionEntity:
    """Fixture for a training definition."""
    training_definition = TrainingDefinitionEntity(
        name="Wednesday Training",
        description="Test training",
        weekday=Weekday.WEDNESDAY,
        period=TimePeriod(
            start=datetime.time(hour=21, minute=0),
            end=datetime.time(hour=22, minute=0),
        ),
        owner=Owner(id=user.id, uuid=user.uuid, name=user.name),
    )
    return await repo.create(training_definition)


def test_create(training_definition: TrainingDefinitionEntity):
    """Test if the training definition was created."""
    assert (
        not training_definition.id.is_empty()
    ), "There should be a training definition created"


async def test_get_by_id(
    repo: TrainingDefinitionRepository, training_definition: TrainingDefinitionEntity
):
    """Test if the training definition can be found with the id."""
    entity = await repo.get_by_id(training_definition.id)

    assert (
        entity.id == training_definition.id
    ), "The training definition should be found"


async def test_get_all(repo: TrainingDefinitionRepository):
    """Test if all training definitions can be loaded."""
    entities = {entity.id: entity async for entity in repo.get_all()}
    assert entities is not None, "There should be a result"


async def test_delete(
    repo: TrainingDefinitionRepository, training_definition: TrainingDefinitionEntity
):
    """Test if the training definition can be deleted."""
    await repo.delete(training_definition)

    with pytest.raises(TrainingDefinitionNotFoundException):
        await repo.get_by_id(training_definition.id)
