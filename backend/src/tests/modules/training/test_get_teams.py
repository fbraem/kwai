"""Module for tests of the get teams use case."""
from kwai.core.db.database import Database
from kwai.modules.training.get_teams import GetTeams
from kwai.modules.training.teams.team_db_repository import TeamDbRepository


async def test_get_teams(database: Database):
    """Test use case get teams."""
    result = await GetTeams(TeamDbRepository(database)).execute()
    assert result is not None
    assert result.count > 0, "There should be a team"
