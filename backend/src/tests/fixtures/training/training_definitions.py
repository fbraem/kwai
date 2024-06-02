"""Module for defining fixture factories for training definitions."""

import pytest
from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.time_period import TimePeriod
from kwai.core.domain.value_objects.weekday import Weekday
from kwai.modules.training.trainings.training_definition import TrainingDefinitionEntity
from kwai.modules.training.trainings.training_definition_db_repository import (
    TrainingDefinitionDbRepository,
)


@pytest.fixture
def make_training_definition(owner: Owner):
    """A factory fixture for creating a training definition."""

    def _make_training_definition(
        name: str | None = None,
        description: str | None = None,
        weekday: Weekday | None = None,
        period: TimePeriod | None = None,
    ) -> TrainingDefinitionEntity:
        return TrainingDefinitionEntity(
            name=name or "A training",
            description=description or "A training definition",
            weekday=weekday or Weekday.MONDAY,
            period=period
            or TimePeriod.create_from_string("18:00", "19:00", "Europe/Brussels"),
            owner=owner,
        )

    return _make_training_definition


@pytest.fixture
def make_training_definition_in_db(
    request, event_loop, database: Database, make_training_definition
):
    """A fixture factory for a training definition in the database."""

    async def _make_training_definition_in_db(
        training_definition: TrainingDefinitionEntity | None = None,
    ) -> TrainingDefinitionEntity:
        training_definition = training_definition or make_training_definition()
        repo = TrainingDefinitionDbRepository(database)
        async with UnitOfWork(database):
            training_definition = await repo.create(training_definition)

        def cleanup():
            async def acleanup():
                async with UnitOfWork(database):
                    await repo.delete(training_definition)

            event_loop.run_until_complete(acleanup())

        request.addfinalizer(cleanup)

        return training_definition

    return _make_training_definition_in_db
