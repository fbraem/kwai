"""Module for testing the use case "Get Story"."""
from kwai.modules.portal.get_story import GetStory, GetStoryCommand
from kwai.modules.portal.news.news_item import NewsItemEntity
from kwai.modules.portal.news.news_item_repository import NewsItemRepository


async def test_get_story(story_repo: NewsItemRepository, saved_story: NewsItemEntity):
    """Test get story."""
    command = GetStoryCommand(id=saved_story.id.value)
    story = await GetStory(story_repo).execute(command)
    assert story is not None, "There should be a story."
