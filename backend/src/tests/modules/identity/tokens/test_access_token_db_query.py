"""Module for testing the access token database query."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.identity.tokens.access_token import AccessTokenIdentifier
from kwai.modules.identity.tokens.access_token_db_query import AccessTokenDbQuery
from kwai.modules.identity.tokens.access_token_query import AccessTokenQuery
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier


@pytest.fixture
def query(database: Database) -> AccessTokenQuery:
    """A fixture for a user account query."""
    return AccessTokenDbQuery(database)


async def test_filter_by_id(query: AccessTokenQuery):
    """Test filtering by id."""
    query.filter_by_id(AccessTokenIdentifier(1))

    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_filter_by_token_identifier(query: AccessTokenQuery):
    """Test filtering by token identifier."""
    query.filter_by_token_identifier(TokenIdentifier.generate())

    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_filter_by_user_account(query: AccessTokenQuery, make_user_account):
    """Test filtering by user account."""
    query.filter_by_user_account(make_user_account())

    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")
