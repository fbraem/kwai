"""Module that tests the Create Team use case."""

import pytest
from kwai.core.db.database import Database
from kwai.modules.teams.create_team import CreateTeam, CreateTeamCommand
from kwai.modules.teams.repositories.team_db_repository import TeamDbRepository

pytestmark = pytest.mark.db


async def test_create_team(database: Database, make_team, team_presenter) -> None:
    """Test the use case 'Create Team'."""
    team = make_team()
    command = CreateTeamCommand(
        name=team.name,
        active=team.is_active,
        remark=team.remark,
    )
    await CreateTeam(TeamDbRepository(database), team_presenter).execute((command))
    assert team_presenter.entity is not None, "The team should be created"
