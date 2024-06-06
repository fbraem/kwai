"""Module for testing the team member repository for a database."""

import pytest
from kwai.core.db.database import Database
from kwai.modules.club.repositories.team_member_db_repository import (
    TeamMemberDbRepository,
)

pytestmark = pytest.mark.db


async def test_get_all(database: Database):
    """Test getting all team members."""
    repo = TeamMemberDbRepository(database)
    team_members = {team_member.id: team_member async for team_member in repo.get_all()}
    assert team_members is not None


async def test_get(database: Database):
    """Test get team member."""
    repo = TeamMemberDbRepository(database)
    team_member = await repo.get()
    assert team_member is not None
