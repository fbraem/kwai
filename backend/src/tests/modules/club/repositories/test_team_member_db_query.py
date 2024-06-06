"""Module for testing the team member query for a database."""

import pytest
from kwai.core.db.database import Database
from kwai.core.domain.value_objects.date import Date
from kwai.modules.club.domain.team_member import TeamMemberIdentifier
from kwai.modules.club.repositories.team_member_db_repository import TeamMemberDbQuery
from kwai.modules.club.repositories.team_member_repository import TeamMemberQuery

pytestmark = pytest.mark.db


@pytest.fixture
def query(database: Database) -> TeamMemberQuery:
    """A fixture for a team member query."""
    return TeamMemberDbQuery(database)


async def test_filter_by_id(query: TeamMemberQuery):
    """Test filtering by id."""
    query.find_by_id(TeamMemberIdentifier(1))
    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_filter_by_birthdate_without_end_date(query: TeamMemberQuery):
    """Test filtering by birthdate."""
    query.find_by_birthdate(Date.create(2015, 1, 1))
    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_filter_by_birthdate(query: TeamMemberQuery):
    """Test filtering by birthdate between two dates."""
    query.find_by_birthdate(Date.create(2015, 1, 1), Date.create(2015, 1, 31))
    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")
