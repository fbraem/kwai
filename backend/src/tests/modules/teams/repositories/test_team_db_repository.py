"""Module for testing the team db repository."""

import pytest
from kwai.core.db.database import Database
from kwai.modules.teams.repositories.team_db_repository import TeamDbRepository
from kwai.modules.teams.repositories.team_repository import TeamNotFoundException

pytestmark = pytest.mark.db


async def test_create_team(make_team_in_db):
    """Test creating a team in the database."""
    team = await make_team_in_db()
    assert team is not None, "There should be a team in the database."


async def test_get_team(database: Database, make_team_in_db):
    """Test getting a team from the database."""
    team = await make_team_in_db()
    repo = TeamDbRepository(database)
    team = repo.get(repo.create_query().filter_by_id(team.id))
    assert team is not None, "There should be a team in the database."


async def test_get_all_teams(database: Database):
    """Test getting all teams in the database."""
    teams_iterator = TeamDbRepository(database).get_all()
    assert teams_iterator is not None, "There should be a team in the database."
    assert (
        await anext(teams_iterator) is not None
    ), "There should be a team in the database."


async def test_delete_team(database: Database, make_team_in_db):
    """Test deleting a team in the database."""
    team_repo = TeamDbRepository(database)
    team = await make_team_in_db()
    await team_repo.delete(team)

    with pytest.raises(TeamNotFoundException):
        await team_repo.get(team_repo.create_query().filter_by_id(team.id))
