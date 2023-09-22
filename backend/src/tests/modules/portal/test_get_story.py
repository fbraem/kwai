"""Module for testing the use case "Get Story"."""
from kwai.modules.portal.get_story import GetStory, GetStoryCommand
from kwai.modules.portal.news.story import StoryEntity
from kwai.modules.portal.news.story_repository import StoryRepository


async def test_get_story(story_repo: StoryRepository, saved_story: StoryEntity):
    """Test get story."""
    command = GetStoryCommand(id=saved_story.id.value)
    story = await GetStory(story_repo).execute(command)
    assert story is not None, "There should be a story."
