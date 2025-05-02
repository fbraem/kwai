"""Module for testing AuthorDbQuery."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.portal.domain.author import AuthorIdentifier
from kwai.modules.portal.repositories.author_db_query import AuthorDbQuery
from kwai.modules.portal.repositories.author_query import AuthorQuery


pytestmark = [pytest.mark.db]


@pytest.fixture(scope="module")
def query(database: Database) -> AuthorQuery:
    """Fixture for creating the author query."""
    return AuthorDbQuery(database)


async def test_filter_by_id(query: AuthorQuery):
    """Test filter by id."""
    query.filter_by_id(AuthorIdentifier(1))
    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_filter_by_uuid(query: AuthorQuery):
    """Test filter by uuid."""
    query.filter_by_uuid(UniqueId.generate())
    try:
        await query.fetch_one()
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")
