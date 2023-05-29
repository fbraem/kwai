"""Module for testing the use case get_stories."""
from types import AsyncGeneratorType

import pytest

from kwai.core.db.database import Database
from kwai.modules.news.get_stories import GetStoriesCommand, GetStories
from kwai.modules.news.stories.story_db_repository import StoryDbRepository
from kwai.modules.news.stories.story_repository import StoryRepository


@pytest.fixture(scope="module")
def repo(database: Database) -> StoryRepository:
    """Create a story repository."""
    return StoryDbRepository(database)


@pytest.mark.asyncio
async def test_get_stories(repo: StoryRepository):
    """Test the use case: get stories."""
    command = GetStoriesCommand()
    count, stories = await GetStories(repo).execute(command)

    assert count >= 0, "Count must be 0 or greater"
    assert isinstance(
        stories, AsyncGeneratorType
    ), "A list of stories should be yielded"

    story_dict = {story.id: story async for story in stories}
    assert count == len(story_dict), "Count should be the same"
