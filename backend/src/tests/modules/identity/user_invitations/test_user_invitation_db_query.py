"""Module for testing UserInvitationDbQuery."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.user_invitations.user_invitation import (
    UserInvitationIdentifier,
)
from kwai.modules.identity.user_invitations.user_invitation_db_query import (
    UserInvitationDbQuery,
)
from kwai.modules.identity.user_invitations.user_invitation_query import (
    UserInvitationQuery,
)


pytestmark = pytest.mark.db


@pytest.fixture(scope="module")
def query(database: Database) -> UserInvitationQuery:
    """Fixture for creating the invitation query."""
    return UserInvitationDbQuery(database)


async def test_filter_by_id(query: UserInvitationQuery):
    """Test the filter by id."""
    query.filter_by_id(UserInvitationIdentifier(1))
    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_filter_by_uuid(query: UserInvitationQuery):
    """Test filter by the unique id."""
    query.filter_by_uuid(UniqueId.generate())
    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_query_filter_by_email(query: UserInvitationQuery):
    """Test the filter by email query."""
    query.filter_by_email(EmailAddress("ichiro.abe@kwai.com"))
    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_query_filter_active(query: UserInvitationQuery):
    """Test the filter active query."""
    query.filter_active()
    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_query_filter_not_expired(query: UserInvitationQuery):
    """Test the filter on not expired."""
    query.filter_not_expired(Timestamp.create_now())
    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_query_filter_not_confirmed(query: UserInvitationQuery):
    """Test the filter on not confirmed."""
    query.filter_not_confirmed()
    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")
