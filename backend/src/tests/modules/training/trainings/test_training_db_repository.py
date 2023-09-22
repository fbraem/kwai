"""Module for testing the training database repository."""

import pytest

from kwai.core.db.database import Database
from kwai.core.db.exceptions import QueryException
from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.period import Period
from kwai.core.domain.value_objects.text import DocumentFormat, Locale, LocaleText
from kwai.modules.training.coaches.coach import CoachEntity, CoachIdentifier
from kwai.modules.training.trainings.training import TrainingEntity
from kwai.modules.training.trainings.training_db_repository import TrainingDbRepository
from kwai.modules.training.trainings.training_definition import TrainingDefinitionEntity
from kwai.modules.training.trainings.training_definition_db_repository import (
    TrainingDefinitionDbRepository,
)
from kwai.modules.training.trainings.training_definition_repository import (
    TrainingDefinitionRepository,
)
from kwai.modules.training.trainings.training_repository import (
    TrainingRepository,
)
from kwai.modules.training.trainings.value_objects import TrainingCoach
from tests.modules.training.conftest import Context

pytestmark = pytest.mark.db


@pytest.fixture(scope="module")
def repo(database: Database) -> TrainingRepository:
    """Fixture for a training repository."""
    return TrainingDbRepository(database)


@pytest.fixture(scope="module")
def training(user, context: Context, owner: Owner) -> TrainingEntity:
    """A fixture for a training."""
    coach = context["coaches"][0]
    person = context["persons"][0]

    text = [
        LocaleText(
            locale=Locale.EN,
            format=DocumentFormat.MARKDOWN,
            title="Training U13",
            summary="Training for U13",
            content="",
            author=owner,
        )
    ]
    return TrainingEntity(
        texts=text,
        period=Period.create_from_delta(hours=1),
        coaches=[
            TrainingCoach(
                coach=CoachEntity(
                    id_=CoachIdentifier(coach.id),
                    name=Name(first_name=person.firstname, last_name=person.lastname),
                    active=True,
                ),
                owner=owner,
                remark="Test Training Coach",
            )
        ],
    )


async def test_create(
    repo: TrainingRepository, context: Context, training: TrainingEntity
):
    """Test create a training."""
    new_training = await repo.create(training)
    assert new_training is not None, "There should be a training."
    context["trainings"] = [new_training]


async def test_update(repo: TrainingRepository, context: Context):
    """Test update of a training."""
    assert len(context["trainings"]) > 0, "There should be a training"
    training = context["trainings"][0]
    updated_training = Entity.replace(training, remark="This training is updated.")
    try:
        await repo.update(updated_training)
    except QueryException as qe:
        pytest.fail(qe)


async def test_get_all(repo: TrainingRepository):
    """Test get all trainings."""
    trainings = {entity.id: entity async for entity in repo.get_all()}
    assert trainings is not None, "There should be a result"


async def test_get_by_id(repo: TrainingRepository, context: Context):
    """Test get training by id."""
    assert len(context["trainings"]) > 0, "There should be a training"
    training = context["trainings"][0]
    training = await repo.get_by_id(training.id)
    assert training is not None, "There should be a result"


async def test_delete(repo: TrainingRepository, context: Context):
    """Test delete of a training."""
    assert len(context["trainings"]) > 0, "There should be a training"
    training = context["trainings"][0]
    try:
        await repo.delete(training)
    except QueryException as qe:
        pytest.fail(qe)


@pytest.fixture(scope="module")
def training_definition_repo(database: Database) -> TrainingDefinitionRepository:
    """Fixture for a training definition repository."""
    return TrainingDefinitionDbRepository(database)


@pytest.fixture
async def saved_training_definition(
    training_definition_repo: TrainingDefinitionRepository,
    training_definition: TrainingDefinitionEntity,
) -> TrainingDefinitionEntity:
    """A fixture for a training definition in the database."""
    return await training_definition_repo.create(training_definition)


async def test_reset_definition(repo: TrainingRepository, saved_training_definition):
    """Test reset definition."""
    await repo.reset_definition(saved_training_definition, False)
