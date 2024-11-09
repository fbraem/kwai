"""Module for testing the TeamMemberDbQuery class."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.teams.domain.team import TeamIdentifier
from kwai.modules.teams.repositories.team_member_db_query import TeamMemberDbQuery


@pytest.fixture
def query(database: Database) -> TeamMemberDbQuery:
    """A fixture for a team member database query."""
    return TeamMemberDbQuery(database)


async def test_filter_by_teams(query: TeamMemberDbQuery):
    """Test filter by teams."""
    query.filter_by_teams(TeamIdentifier(1))
    try:
        await query.fetch_team_members()
    except Exception as exc:
        pytest.fail(f"An exception occurred: f{exc}")
