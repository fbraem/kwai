"""Module for testing the members database query."""
import pytest

from kwai.core.db.database import Database
from kwai.modules.club.members.member import MemberIdentifier
from kwai.modules.club.members.member_db_query import MemberDbQuery


async def test_filter_by_id(database: Database):
    """Test filtering by id."""
    query = MemberDbQuery(database)
    query.filter_by_id(MemberIdentifier(1))

    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_filter_by_license(database: Database):
    """Test filtering by license."""
    query = MemberDbQuery(database)
    query.filter_by_license("12345678")

    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")
