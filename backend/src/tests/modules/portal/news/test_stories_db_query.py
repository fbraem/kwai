"""Module for testing the story database query."""
import pytest

from kwai.core.db.database import Database
from kwai.modules.portal.news.story_db_query import StoryDbQuery

pytestmark = pytest.mark.db


async def test_story_db_query(database: Database):
    """Test the query."""
    query = StoryDbQuery(database)
    count = await query.count()
    assert count >= 0, "There should be 0 or more stories."
    rows = query.order_by_publication_date().fetch(limit=10)
    assert rows is not None, "There should be a result"


async def test_filter_by_publication_date(database: Database):
    """Test the query with filtering on the story publication date."""
    query = StoryDbQuery(database)
    query.filter_by_publication_date(2023)
    count = await query.count()
    assert count >= 0, "There should be 0 or more stories."


async def test_filter_by_promoted(database: Database):
    """Test the query with filtering on promoted stories."""
    query = StoryDbQuery(database)
    query.filter_by_promoted()
    count = await query.count()
    assert count >= 0, "There should be 0 or more stories."


async def test_filter_by_active(database: Database):
    """Test the query with filtering on active stories."""
    query = StoryDbQuery(database)
    query.filter_by_active()
    count = await query.count()
    assert count >= 0, "There should be 0 or more stories."


async def test_filter_by_user(database: Database):
    """Test the query with filtering on author."""
    query = StoryDbQuery(database)
    query.filter_by_user(1)
    count = await query.count()
    assert count >= 0, "There should be 0 or more stories."
