"""Module for testing the news item database query."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.portal.news.news_item_db_query import NewsItemDbQuery

pytestmark = pytest.mark.db


async def test_news_item_db_query(database: Database):
    """Test the query."""
    query = NewsItemDbQuery(database)
    count = await query.count()
    assert count >= 0, "There should be 0 or more news items."
    rows = query.order_by_publication_date().fetch(limit=10)
    assert rows is not None, "There should be a result"


async def test_filter_by_publication_date(database: Database):
    """Test the query with filtering on the news item publication date."""
    query = NewsItemDbQuery(database)
    query.filter_by_publication_date(2023)
    count = await query.count()
    assert count >= 0, "There should be 0 or more news items."


async def test_filter_by_promoted(database: Database):
    """Test the query with filtering on promoted news items."""
    query = NewsItemDbQuery(database)
    query.filter_by_promoted()
    count = await query.count()
    assert count >= 0, "There should be 0 or more news items."


async def test_filter_by_active(database: Database):
    """Test the query with filtering on active news items."""
    query = NewsItemDbQuery(database)
    query.filter_by_active()
    count = await query.count()
    assert count >= 0, "There should be 0 or more news items."


async def test_filter_by_user(database: Database):
    """Test the query with filtering on author."""
    query = NewsItemDbQuery(database)
    query.filter_by_user(1)
    count = await query.count()
    assert count >= 0, "There should be 0 or more news items."
