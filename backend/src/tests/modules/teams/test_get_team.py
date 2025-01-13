"""Module for defining tests for the use case 'Get Teams'."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.teams.get_team import GetTeam, GetTeamCommand
from kwai.modules.teams.repositories.team_db_repository import TeamDbRepository


pytestmark = pytest.mark.db


async def test_get_teams(database: Database, make_team_in_db, team_presenter):
    """Test get teams."""
    team = await make_team_in_db()
    command = GetTeamCommand(id=team.id.value)
    await GetTeam(TeamDbRepository(database), team_presenter).execute(command)
    assert team_presenter.entity is not None, "The team should exist"
    assert team_presenter.entity.id == team.id, "The team should be found"
