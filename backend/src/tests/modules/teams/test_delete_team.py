"""Module for testing the Delete Team use case."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.teams.delete_team import DeleteTeam, DeleteTeamCommand
from kwai.modules.teams.repositories.team_db_repository import TeamDbRepository
from kwai.modules.teams.repositories.team_repository import TeamNotFoundException


pytestmark = pytest.mark.db


async def test_delete_team(database: Database, make_team_in_db):
    """Test deleting a team."""
    team = await make_team_in_db()
    command = DeleteTeamCommand(id=team.id.value)
    team_repo = TeamDbRepository(database)
    await DeleteTeam(team_repo).execute(command)

    with pytest.raises(TeamNotFoundException):
        await team_repo.get(team_repo.create_query().filter_by_id(team.id))
