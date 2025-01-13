"""Module for testing the news item database repository."""

import pytest

from kwai.modules.portal.news.news_item_repository import (
    NewsItemNotFoundException,
)


pytestmark = pytest.mark.db


async def test_create(saved_news_item):
    """Test if the creation was successful."""
    assert not saved_news_item.id.is_empty(), "There should be a news item created"


async def test_get_all(news_item_repo, saved_news_item):
    """Test for get_all."""
    stories = {entity.id: entity async for entity in news_item_repo.get_all()}
    assert saved_news_item.id in stories, (
        f"The news item with id {saved_news_item.id} should be present"
    )


async def test_get_by_id(news_item_repo, saved_news_item):
    """Test for get_by_id."""
    entity = await news_item_repo.get_by_id(saved_news_item.id)
    assert entity is not None, (
        f"There should be a news item with id {saved_news_item.id}"
    )


async def test_delete(news_item_repo, saved_news_item):
    """Test the deletion of a news item."""
    await news_item_repo.delete(saved_news_item)

    with pytest.raises(NewsItemNotFoundException):
        await news_item_repo.get_by_id(saved_news_item.id)
