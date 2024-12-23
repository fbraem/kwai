"""Module for tests of the get teams use case."""

from kwai.core.db.database import Database
from kwai.modules.training.get_teams import GetTeams
from kwai.modules.training.teams.team_db_repository import TeamDbRepository


async def test_get_teams(database: Database, make_team_in_db):
    """Test use case get teams."""
    team = await make_team_in_db()
    count, iterator = await GetTeams(TeamDbRepository(database)).execute()
    assert count > 0, "There should be a team"
    teams = {team.id: team async for team in iterator}
    assert team.id in teams, "The team should be in the result"
