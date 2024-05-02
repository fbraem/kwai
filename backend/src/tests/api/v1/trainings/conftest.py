"""Module that defines fixtures for testing the trainings endpoints."""

from datetime import time

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.period import Period
from kwai.core.domain.value_objects.text import DocumentFormat, Locale, LocaleText
from kwai.core.domain.value_objects.time_period import TimePeriod
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.core.domain.value_objects.weekday import Weekday
from kwai.modules.training.trainings.training import TrainingEntity
from kwai.modules.training.trainings.training_db_repository import TrainingDbRepository
from kwai.modules.training.trainings.training_definition import TrainingDefinitionEntity
from kwai.modules.training.trainings.training_definition_db_repository import (
    TrainingDefinitionDbRepository,
)


@pytest.fixture
async def training_entity(database: Database, owner: Owner) -> TrainingEntity:
    """A fixture for a training in the database."""
    repo = TrainingDbRepository(database)
    return await repo.create(
        TrainingEntity(
            texts=[
                LocaleText(
                    locale=Locale.NL,
                    format=DocumentFormat.MARKDOWN,
                    content="This is a test training",
                    summary="Test API training",
                    title="Test API Training",
                    author=owner,
                )
            ],
            period=Period.create_from_delta(
                Timestamp.create_from_string("2023-01-02 20:00:00"), hours=2
            ),
            remark="Created as fixture for testing endpoint trainings",
        )
    )


@pytest.fixture
async def training_definition_entity(
    database: Database, owner: Owner
) -> TrainingDefinitionEntity:
    """A fixture for a training definition."""
    repo = TrainingDefinitionDbRepository(database)
    return await repo.create(
        TrainingDefinitionEntity(
            name="Test training definition",
            description="A training definition for testing",
            weekday=Weekday.MONDAY,
            period=TimePeriod(start=time(hour=19), end=time(hour=20)),
            remark="This is a test",
            owner=owner,
        )
    )
