"""Module for testing the team database repository."""
import pytest

from kwai.core.db.database import Database
from kwai.core.db.exceptions import QueryException
from kwai.modules.training.teams.team import TeamIdentifier
from kwai.modules.training.teams.team_db_repository import TeamDbRepository


async def test_get_by_ids(database: Database):
    """Test get_by_ids method."""
    repo = TeamDbRepository(database)

    try:
        {
            team.id: team
            async for team in repo.get_by_ids(TeamIdentifier(1), TeamIdentifier(2))
        }
    except QueryException as qe:
        pytest.fail(str(qe))


async def test_get_all(database: Database):
    """Test get_all."""
    repo = TeamDbRepository(database)

    try:
        repo.get_all()
    except QueryException as qe:
        pytest.fail(str(qe))
