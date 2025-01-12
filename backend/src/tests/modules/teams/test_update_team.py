"""Module for testing the 'Update Team' use case."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.teams.repositories.team_db_repository import TeamDbRepository
from kwai.modules.teams.update_team import UpdateTeam, UpdateTeamCommand

pytestmark = pytest.mark.db


async def test_update_team(database: Database, make_team_in_db, team_presenter):
    """Test the use case 'Update Team'."""
    team = await make_team_in_db()
    command = UpdateTeamCommand(
        id=team.id.value,
        name=team.name,
        active=team.is_active,
        remark="This is a test.",
    )
    await UpdateTeam(TeamDbRepository(database), team_presenter).execute(command)
    assert team_presenter.entity.remark == "This is a test.", (
        "The team should be updated."
    )
