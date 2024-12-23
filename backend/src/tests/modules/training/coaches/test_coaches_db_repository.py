"""Module for testing the coach database repository."""

import pytest

from kwai.core.db.database import Database
from kwai.core.db.exceptions import QueryException
from kwai.modules.training.coaches.coach_db_repository import CoachDbRepository


async def test_get_by_id(database: Database, make_coach_in_db):
    """Test get_by_id method."""
    coach = await make_coach_in_db()
    repo = CoachDbRepository(database)

    try:
        await repo.get_by_id(coach.id)
    except QueryException as qe:
        pytest.fail(str(qe))


async def test_get_by_ids(database: Database, make_coach_in_db):
    """Test get_by_ids method."""
    repo = CoachDbRepository(database)
    coach_1 = await make_coach_in_db()
    coach_2 = await make_coach_in_db()

    try:
        {coach.id: coach async for coach in repo.get_by_ids(coach_1.id, coach_2.id)}
    except QueryException as qe:
        pytest.fail(str(qe))


async def test_get_all(database: Database, make_coach_in_db):
    """Test get_all method."""
    await make_coach_in_db()
    repo = CoachDbRepository(database)

    try:
        repo.get_all()
    except QueryException as qe:
        pytest.fail(str(qe))
