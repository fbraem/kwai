"""Module for testing the news item database repository."""

import pytest

from kwai.modules.portal.news.news_item import (
    NewsItemEntity,
)
from kwai.modules.portal.news.news_item_repository import (
    NewsItemNotFoundException,
    NewsItemRepository,
)

pytestmark = pytest.mark.db


async def test_create(saved_story: NewsItemEntity):
    """Test if the creation was successful."""
    assert not saved_story.id.is_empty(), "There should be a news item created"


async def test_get_all(story_repo: NewsItemRepository, saved_story: NewsItemEntity):
    """Test for get_all."""
    stories = {entity.id: entity async for entity in story_repo.get_all()}
    assert (
        saved_story.id in stories
    ), f"The story with id {saved_story.id} should be present"


async def test_get_by_id(story_repo: NewsItemRepository, saved_story: NewsItemEntity):
    """Test for get_by_id."""
    entity = await story_repo.get_by_id(saved_story.id)
    assert entity is not None, f"There should be a news item with id {saved_story.id}"


async def test_delete(story_repo: NewsItemRepository, saved_story: NewsItemEntity):
    """Test the deletion of a news item."""
    await story_repo.delete(saved_story)

    with pytest.raises(NewsItemNotFoundException):
        await story_repo.get_by_id(saved_story.id)
