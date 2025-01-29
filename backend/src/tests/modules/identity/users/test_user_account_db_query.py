"""Module for testing the user account database query."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.users.user_account import UserAccountIdentifier
from kwai.modules.identity.users.user_account_db_query import UserAccountDbQuery
from kwai.modules.identity.users.user_account_query import UserAccountQuery


pytestmark = pytest.mark.db


@pytest.fixture
def query(database: Database) -> UserAccountQuery:
    """A fixture for a user account query."""
    return UserAccountDbQuery(database)


async def test_filter_by_id(query: UserAccountQuery):
    """Test filtering by id."""
    query.filter_by_id(UserAccountIdentifier(1))

    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_filter_by_email(query: UserAccountQuery):
    """Test filtering by email."""
    query.filter_by_email(EmailAddress(email="jigoro.kano@kwai.com"))

    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_filter_by_uuid(query: UserAccountQuery):
    """Test filtering by unique id."""
    query.filter_by_uuid(UniqueId.generate())

    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")
