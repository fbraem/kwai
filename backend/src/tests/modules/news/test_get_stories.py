"""Module for testing the use case get_stories."""
from types import AsyncGeneratorType

import pytest

from kwai.core.db.database import Database
from kwai.modules.news.get_stories import GetStories, GetStoriesCommand
from kwai.modules.news.stories.story_db_repository import StoryDbRepository
from kwai.modules.news.stories.story_repository import StoryRepository

pytestmark = pytest.mark.db


@pytest.fixture(scope="module")
def repo(database: Database) -> StoryRepository:
    """Create a story repository."""
    return StoryDbRepository(database)


async def test_get_stories(repo: StoryRepository):
    """Test the use case: get stories."""
    command = GetStoriesCommand()
    count, story_iterator = await GetStories(repo).execute(command)

    assert count >= 0, "Count must be 0 or greater"
    assert isinstance(
        story_iterator, AsyncGeneratorType
    ), "A list of stories should be yielded"

    story_dict = {story.id: story async for story in story_iterator}
    assert count == len(story_dict), "Count should be the same"
