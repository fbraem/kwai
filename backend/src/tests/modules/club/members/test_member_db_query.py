"""Module for testing the members database query."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.club.members.member import MemberIdentifier
from kwai.modules.club.members.member_db_query import MemberDbQuery
from kwai.modules.club.members.member_query import MemberQuery


@pytest.fixture
def query(database: Database) -> MemberQuery:
    """A fixture for a member query."""
    return MemberDbQuery(database)


async def test_filter_by_id(query: MemberQuery):
    """Test filtering by id."""
    query.filter_by_id(MemberIdentifier(1))

    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_filter_by_license(query: MemberQuery):
    """Test filtering by license."""
    query.filter_by_license("12345678")

    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_filter_by_active(query: MemberQuery):
    """Test filtering by active."""
    query.filter_by_active()

    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_filter_by_license_date(query: MemberQuery):
    """Test filtering by license date."""
    query.filter_by_license_date(1, 2024)

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
