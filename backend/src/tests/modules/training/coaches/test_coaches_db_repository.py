"""Module for testing the coach database repository."""
import pytest

from kwai.core.db.database import Database
from kwai.core.db.exceptions import QueryException
from kwai.modules.training.coaches.coach import CoachIdentifier
from kwai.modules.training.coaches.coach_db_repository import CoachDbRepository


async def test_get_by_id(database: Database):
    """Test get_by_id method."""
    repo = CoachDbRepository(database)

    try:
        await repo.get_by_id(CoachIdentifier(1))
    except QueryException as qe:
        pytest.fail(str(qe))
