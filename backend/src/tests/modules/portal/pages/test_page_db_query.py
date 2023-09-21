"""Module for testing page database query."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.portal.pages.page_db_query import PageDbQuery
from kwai.modules.portal.pages.page_query import PageQuery


@pytest.fixture
def page_query(database: Database) -> PageQuery:
    """Fixture for a page query."""
    return PageDbQuery(database)


async def test_page_db_query(page_query: PageQuery):
    """Test the query."""
    count = await page_query.count()
    assert count >= 0, "There should be 0 or more pages."


async def test_filter_by_active(page_query: PageQuery):
    """Test the query with filtering on active pages."""
    query = page_query.filter_by_active()
    count = await query.count()
    assert count >= 0, "There should be 0 or more pages."


async def test_filter_by_user(page_query: PageQuery):
    """Test the query with filtering on author."""
    page_query.filter_by_user(1)
    count = await page_query.count()
    assert count >= 0, "There should be 0 or more stories."
