"""Module for testing the team member query for a database."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.date import Date
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.teams.domain.team import TeamIdentifier
from kwai.modules.teams.domain.team_member import MemberIdentifier
from kwai.modules.teams.repositories.member_db_repository import MemberDbQuery
from kwai.modules.teams.repositories.member_repository import MemberQuery

pytestmark = pytest.mark.db


@pytest.fixture
def query(database: Database) -> MemberQuery:
    """A fixture for a team member query."""
    return MemberDbQuery(database)


async def test_filter_by_id(query: MemberQuery):
    """Test filtering by id."""
    query.filter_by_id(MemberIdentifier(1))
    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_filter_by_uuid(query: MemberQuery):
    """Test filtering by uuid."""
    query.filter_by_uuid(UniqueId.generate())
    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_filter_by_birthdate_without_end_date(query: MemberQuery):
    """Test filtering by birthdate."""
    query.filter_by_birthdate(Date.create(2015, 1, 1))
    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_filter_by_birthdate(query: MemberQuery):
    """Test filtering by birthdate between two dates."""
    query.filter_by_birthdate(Date.create(2015, 1, 1), Date.create(2015, 1, 31))
    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_filter_by_team(query: MemberQuery):
    """Test filtering by not part of the team."""
    query.filter_by_team(TeamIdentifier(1))
    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_filter_by_not_in_team(query: MemberQuery):
    """Test filtering by not part of the team."""
    query.filter_by_team(TeamIdentifier(1))
    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")
