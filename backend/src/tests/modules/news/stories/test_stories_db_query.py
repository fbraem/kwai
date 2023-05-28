"""Module for testing the story database query."""
import pytest

from kwai.core.db.database import Database
from kwai.modules.news.stories.story_db_query import StoryDbQuery


@pytest.mark.asyncio
async def test_story_db_query(database: Database):
    """Test the query."""
    query = StoryDbQuery(database)
    query.filter_by_active()
    count = await query.count()
    assert count > 0, "There should be some stories..."
    rows = query.order_by_publication_date().fetch(limit=10)
    assert rows is not None, "There should be a result"

    row = await anext(rows)
    assert row is not None, "There should be a row"
    print(row)
