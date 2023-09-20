"""Module for defining fixtures used for testing the page module."""
import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.text import DocumentFormat, Locale, LocaleText
from kwai.modules.page.pages.page import Application, PageEntity
from kwai.modules.portal.applications.application import ApplicationEntity
from kwai.modules.portal.applications.application_db_repository import (
    ApplicationDbRepository,
)


@pytest.fixture(scope="module")
async def application(database: Database) -> Application:
    """Fixture for an application."""
    repo = ApplicationDbRepository(database)
    application = ApplicationEntity(
        title="Test", name="test", short_description="An application used for testing"
    )
    application = await repo.create(application)

    yield Application(id=application.id, name=application.name, title=application.title)

    await repo.delete(application)


@pytest.fixture(scope="module")
def page(owner: Owner, application: Application) -> PageEntity:
    """Fixture for a page."""
    return PageEntity(
        enabled=True,
        application=application,
        content=[
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
