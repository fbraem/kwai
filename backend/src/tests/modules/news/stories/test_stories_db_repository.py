"""Module for testing the story database repository."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.news.stories.story import (
    StoryEntity,
    Content,
    Author,
    Application,
)
from kwai.modules.news.stories.story_db_repository import StoryDbRepository
from kwai.modules.news.stories.story_repository import (
    StoryRepository,
    StoryNotFoundException,
)


@pytest.fixture(scope="module")
async def repo(database: Database) -> StoryRepository:
    """Fixture for a story repository."""
    return StoryDbRepository(database)


@pytest.fixture(scope="module")
async def story(
    repo: StoryRepository, author: Author, application: Application
) -> StoryEntity:
    """Fixture for a story."""
    story = StoryEntity(
        content=[
            Content(
                format="md",
                locale="nl",
                title="test",
                content="This is a test",
                summary="This is a summary of the test",
                author=author,
            )
        ],
        application=application,
    )
    return await repo.create(story)


@pytest.mark.asyncio
async def test_create(story: StoryEntity):
    """Test if the creation was successful."""
    assert not story.id.is_empty(), "There should be a story created"


@pytest.mark.asyncio
async def test_get_all(repo: StoryRepository, story: StoryEntity):
    """Test for get_all."""
    stories = {entity.id: entity async for entity in repo.get_all()}
    assert story.id in stories, f"The story with id {story.id} should be present"


@pytest.mark.asyncio
async def test_get_by_id(repo: StoryRepository, story: StoryEntity):
    """Test for get_by_id."""
    entity = await repo.get_by_id(story.id)
    assert entity is not None, f"There should be a story with id {story.id}"


@pytest.mark.asyncio
async def test_delete(repo: StoryRepository, story: StoryEntity):
    """Test the deletion of a story."""
    await repo.delete(story)

    with pytest.raises(StoryNotFoundException):
        await repo.get_by_id(story.id)
