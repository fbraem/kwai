"""Module for testing the coach database repository."""
import pytest

from kwai.core.db.database import Database
from kwai.core.db.exceptions import QueryException
from kwai.modules.training.coaches.coach import CoachIdentifier
from kwai.modules.training.coaches.coach_db_repository import CoachDbRepository
from kwai.modules.training.coaches.coach_repository import CoachNotFoundException


async def test_get_by_id(database: Database):
    """Test get_by_id method."""
    repo = CoachDbRepository(database)

    try:
        await repo.get_by_id(CoachIdentifier(1))
    except CoachNotFoundException:
        pass  # Ok
    except QueryException as qe:
        pytest.fail(str(qe))


async def test_get_by_ids(database: Database):
    """Test get_by_ids method."""
    repo = CoachDbRepository(database)

    try:
        coaches = {
            coach.id: coach
            async for coach in repo.get_by_ids(CoachIdentifier(1), CoachIdentifier(2))
        }
    except CoachNotFoundException:
        pass  # Ok
    except QueryException as qe:
        pytest.fail(str(qe))
