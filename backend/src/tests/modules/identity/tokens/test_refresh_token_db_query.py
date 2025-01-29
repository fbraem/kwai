"""Module for testing the refresh token database query."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.identity.tokens.refresh_token import RefreshTokenIdentifier
from kwai.modules.identity.tokens.refresh_token_db_query import RefreshTokenDbQuery
from kwai.modules.identity.tokens.refresh_token_query import RefreshTokenQuery
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier


@pytest.fixture
def query(database: Database) -> RefreshTokenQuery:
    """A fixture for a user account query."""
    return RefreshTokenDbQuery(database)


async def test_filter_by_id(query: RefreshTokenQuery):
    """Test filtering by id."""
    query.filter_by_id(RefreshTokenIdentifier(1))

    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_filter_by_token_identifier(query: RefreshTokenQuery):
    """Test filtering by token identifier."""
    query.filter_by_token_identifier(TokenIdentifier.generate())

    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_filter_by_user_account(query: RefreshTokenQuery, make_user_account):
    """Test filtering by user account."""
    query.filter_by_user_account(make_user_account())

    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")
