"""Module for testing the news item database repository."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.text import DocumentFormat, Locale, LocaleText
from kwai.modules.portal.applications.application import ApplicationEntity
from kwai.modules.portal.news.news_item import (
    NewsItemEntity,
)
from kwai.modules.portal.news.news_item_db_repository import NewsItemDbRepository
from kwai.modules.portal.news.news_item_repository import (
    NewsItemNotFoundException,
    NewsItemRepository,
)

pytestmark = pytest.mark.db


@pytest.fixture(scope="module")
async def repo(database: Database) -> NewsItemRepository:
    """Fixture for a news story repository."""
    return NewsItemDbRepository(database)


@pytest.fixture(scope="module")
async def story(
    repo: NewsItemRepository, owner: Owner, application: ApplicationEntity
) -> NewsItemEntity:
    """Fixture for a news item."""
    story = NewsItemEntity(
        texts=[
            LocaleText(
                format=DocumentFormat.MARKDOWN,
                locale=Locale.NL,
                title="test",
                content="This is a test",
                summary="This is a summary of the test",
                author=owner,
            )
        ],
        application=application,
    )
    return await repo.create(story)


async def test_create(story: NewsItemEntity):
    """Test if the creation was successful."""
    assert not story.id.is_empty(), "There should be a story created"


async def test_get_all(repo: NewsItemRepository, story: NewsItemEntity):
    """Test for get_all."""
    stories = {entity.id: entity async for entity in repo.get_all()}
    assert story.id in stories, f"The story with id {story.id} should be present"


async def test_get_by_id(repo: NewsItemRepository, story: NewsItemEntity):
    """Test for get_by_id."""
    entity = await repo.get_by_id(story.id)
    assert entity is not None, f"There should be a news item with id {story.id}"


async def test_delete(repo: NewsItemRepository, story: NewsItemEntity):
    """Test the deletion of a news item."""
    await repo.delete(story)

    with pytest.raises(NewsItemNotFoundException):
        await repo.get_by_id(story.id)
