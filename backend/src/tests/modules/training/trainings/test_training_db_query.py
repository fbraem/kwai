"""Module for testing TrainingDbQuery."""
from datetime import datetime, time, timedelta

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.time_period import TimePeriod
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.core.domain.value_objects.weekday import Weekday
from kwai.modules.training.coaches.coach import CoachEntity
from kwai.modules.training.trainings.training import TrainingIdentifier
from kwai.modules.training.trainings.training_db_query import TrainingDbQuery
from kwai.modules.training.trainings.training_definition import (
    TrainingDefinitionEntity,
    TrainingDefinitionIdentifier,
)
from kwai.modules.training.trainings.value_objects import Team

pytestmark = pytest.mark.db


@pytest.mark.asyncio
async def test_filter_by_id(database: Database):
    """Test filtering on id."""
    query = TrainingDbQuery(database)
    query.filter_by_id(TrainingIdentifier(1))

    count = await query.count()
    assert count >= 0, "There should be 0 or more trainings."


@pytest.mark.asyncio
async def test_filter_by_year(database: Database):
    """Test filtering on id."""
    query = TrainingDbQuery(database)
    query.filter_by_year_month(2022)

    count = await query.count()
    assert count >= 0, "There should be 0 or more trainings."


@pytest.mark.asyncio
async def test_filter_by_year_month(database: Database):
    """Test filtering on id."""
    query = TrainingDbQuery(database)
    query.filter_by_year_month(2022, 1)

    count = await query.count()
    assert count >= 0, "There should be 0 or more trainings."


@pytest.mark.asyncio
async def test_filter_by_dates(database: Database):
    """Test filtering on dates."""
    query = TrainingDbQuery(database)
    query.filter_by_dates(datetime.utcnow(), datetime.utcnow() + timedelta(days=1))
    count = await query.count()
    assert count >= 0, "There should be 0 or more trainings."


@pytest.mark.asyncio
async def test_filter_by_coach(database: Database):
    """Test filtering on coach."""
    query = TrainingDbQuery(database)
    query.filter_by_coach(
        CoachEntity(
            id_=IntIdentifier(1),
            name=Name(first_name="Jigoro", last_name="Kano"),
            active=True,
        )
    )
    count = await query.count()
    assert count >= 0, "There should be 0 or more trainings."


async def test_filter_by_team(database: Database):
    """Test filtering on team."""
    query = TrainingDbQuery(database)
    query.filter_by_team(Team(id=IntIdentifier(1), name="U18"))
    count = await query.count()
    assert count >= 0, "There should be 0 or more trainings."


async def test_filter_by_definition(database: Database):
    """Test filtering on definition."""
    query = TrainingDbQuery(database)
    query.filter_by_definition(
        TrainingDefinitionEntity(
            id_=TrainingDefinitionIdentifier(1),
            name="Test",
            description="Test",
            weekday=Weekday.MONDAY,
            owner=Owner(
                id=IntIdentifier(1),
                uuid=UniqueId.generate(),
                name=Name(first_name="Jigoro", last_name="Kano"),
            ),
            period=TimePeriod(start=time(hour=20), end=time(hour=21)),
        )
    )
    count = await query.count()
    assert count >= 0, "There should be 0 or more trainings."


@pytest.mark.asyncio
async def test_filter_active(database: Database):
    """Test filtering only active trainings."""
    query = TrainingDbQuery(database)
    query.filter_active()

    count = await query.count()
    assert count >= 0, "There should be 0 or more trainings."
