"""Module for testing the page database repository."""
import pytest

from kwai.core.db.database import Database
from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.text import DocumentFormat, Locale, LocaleText
from kwai.modules.page.pages.page import Application, PageEntity
from kwai.modules.page.pages.page_db_repository import PageDbRepository
from kwai.modules.page.pages.page_repository import PageRepository


@pytest.fixture(scope="module")
def repo(database: Database) -> PageRepository:
    """Fixture for a page repository."""
    return PageDbRepository(database)


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


@pytest.fixture(scope="module")
async def saved_page(repo: PageRepository, page: PageEntity) -> PageEntity:
    """Fixture for a page stored in the database."""
    return await repo.create(page)


async def test_create(repo: PageRepository, saved_page: PageEntity):
    """Test create page."""
    assert not saved_page.id.is_empty(), "There should be an id for a new page."


async def test_get_all(repo: PageRepository, saved_page: PageEntity):
    """Test get all pages."""
    page_iterator = repo.get_all()
    page = await anext(page async for page in page_iterator if page.id == saved_page.id)
    assert page is not None, "Page should be available"
    assert page.id == saved_page.id, f"Page should have id {saved_page.id}"


async def test_get_by_id(repo: PageRepository, saved_page: PageEntity):
    """Test get by id."""
    page = await repo.get_by_id(saved_page.id)
    assert page is not None, "There should be a page."


async def test_update(repo: PageRepository, saved_page: PageEntity):
    """Test update page."""
    changed_page = Entity.replace(saved_page, remark="This is an update.")
    await repo.update(changed_page)
    page = await repo.get_by_id(changed_page.id)
    assert page.remark == "This is an update.", "The page should be updated."
