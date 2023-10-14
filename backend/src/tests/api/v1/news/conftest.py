"""Module for defining fixtures for the news API."""
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
from kwai.modules.portal.news.news_item import NewsItemEntity
from kwai.modules.portal.news.news_item_db_repository import NewsItemDbRepository


@pytest.fixture(scope="module")
def application_repo(database: Database) -> ApplicationRepository:
    """Fixture for an application repository."""
    return ApplicationDbRepository(database)


@pytest.fixture(scope="module")
async def application(application_repo: ApplicationRepository) -> ApplicationEntity:
    """Fixture for an application."""
    application = ApplicationEntity(
        title="News Test",
        name="news_test",
        short_description="An application used for testing",
    )
    application = await application_repo.create(application)

    yield application

    await application_repo.delete(application)


@pytest.fixture
async def news_item_entity(
    database: Database, application: ApplicationEntity, owner: Owner
) -> NewsItemEntity:
    """A fixture for a news entity in the database."""
    repo = NewsItemDbRepository(database)
    return await repo.create(
        NewsItemEntity(
            enabled=True,
            application=application,
            texts=[
                LocaleText(
                    locale=Locale.EN,
                    format=DocumentFormat.MARKDOWN,
                    title="Test News Item",
                    summary="This is a test news item",
                    content="This is a test news item",
                    author=owner,
                )
            ],
            remark="Test news item.",
        )
    )
