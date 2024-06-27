"""Module for testing the team db repository."""

import pytest
from kwai.core.db.database import Database
from kwai.modules.teams.repositories.team_db_repository import TeamDbRepository

pytestmark = pytest.mark.db


async def test_create_team(make_team_in_db):
    """Test creating a team in the database."""
    team = await make_team_in_db()
    assert team is not None, "There should be a team in the database."


async def test_get_all_teams(database: Database):
    """Test getting all teams in the database."""
    teams_iterator = TeamDbRepository(database).get_all()
    assert teams_iterator is not None, "There should be a team in the database."

    async for team in teams_iterator:
        print(team)
