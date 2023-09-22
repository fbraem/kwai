"""Module for defining fixtures used for testing the page module."""
import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.text import DocumentFormat, Locale, LocaleText
from kwai.modules.portal.applications.application import ApplicationEntity
from kwai.modules.portal.applications.application_db_repository import (
    ApplicationDbRepository,
)
from kwai.modules.portal.applications.application_repository import (
    ApplicationRepository,
)
from kwai.modules.portal.news.news_item import StoryEntity
from kwai.modules.portal.news.news_item_db_repository import StoryDbRepository
from kwai.modules.portal.news.news_item_repository import StoryRepository
from kwai.modules.portal.pages.page import PageEntity
from kwai.modules.portal.pages.page_db_repository import PageDbRepository
from kwai.modules.portal.pages.page_repository import PageRepository


@pytest.fixture(scope="module")
def application_repo(database: Database) -> ApplicationRepository:
    """Fixture for an application repository."""
    return ApplicationDbRepository(database)


@pytest.fixture(scope="module")
async def application(application_repo: ApplicationRepository) -> ApplicationEntity:
    """Fixture for an application."""
    application = ApplicationEntity(
        title="Test", name="test", short_description="An application used for testing"
    )
    application = await application_repo.create(application)

    yield application

    await application_repo.delete(application)


@pytest.fixture(scope="module")
def page(owner: Owner, application: ApplicationEntity) -> PageEntity:
    """Fixture for a page."""
    return PageEntity(
        enabled=True,
        application=application,
        texts=[
            LocaleText(
                format=DocumentFormat.MARKDOWN,
                locale=Locale.EN,
                title="Test",
                content="This is a test",
                summary="This is a summary",
                author=owner,
            )
        ],
        priority=0,
        remark="Test",
    )


@pytest.fixture(scope="module")
def page_repo(database: Database) -> PageRepository:
    """Fixture for a page repository."""
    return PageDbRepository(database)


@pytest.fixture(scope="module")
async def saved_page(page_repo: PageRepository, page: PageEntity) -> PageEntity:
    """Fixture for a page stored in the database."""
    return await page_repo.create(page)


@pytest.fixture(scope="module")
def story_repo(database: Database) -> StoryRepository:
    """Fixture for a story repository."""
    return StoryDbRepository(database)


@pytest.fixture(scope="module")
def story(owner: Owner, application: ApplicationEntity) -> StoryEntity:
    """Fixture for a story entity."""
    return StoryEntity(
        enabled=True,
        application=application,
        texts=[
            LocaleText(
                locale=Locale.EN,
                format=DocumentFormat.MARKDOWN,
                title="Test Story",
                summary="This is a test story",
                content="This is a test story",
                author=owner,
            )
        ],
        remark="Test story.",
    )


@pytest.fixture(scope="module")
async def saved_story(story_repo: StoryRepository, story: StoryEntity) -> StoryEntity:
    """Fixture for a story in the database."""
    return await story_repo.create(story)
