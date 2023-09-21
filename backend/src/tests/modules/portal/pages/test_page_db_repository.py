"""Module for testing the page database repository."""

from kwai.core.domain.entity import Entity
from kwai.modules.portal.pages.page import PageEntity
from kwai.modules.portal.pages.page_repository import PageRepository


async def test_create(saved_page: PageEntity):
    """Test create page."""
    assert not saved_page.id.is_empty(), "There should be an id for a new page."


async def test_get_all(page_repo: PageRepository, saved_page: PageEntity):
    """Test get all pages."""
    page_iterator = page_repo.get_all()
    page = await anext(page async for page in page_iterator if page.id == saved_page.id)
    assert page is not None, "Page should be available"
    assert page.id == saved_page.id, f"Page should have id {saved_page.id}"


async def test_get_by_id(page_repo: PageRepository, saved_page: PageEntity):
    """Test get by id."""
    page = await page_repo.get_by_id(saved_page.id)
    assert page is not None, "There should be a page."


async def test_update(page_repo: PageRepository, saved_page: PageEntity):
    """Test update page."""
    changed_page = Entity.replace(saved_page, remark="This is an update.")
    await page_repo.update(changed_page)
    page = await page_repo.get_by_id(changed_page.id)
    assert page.remark == "This is an update.", "The page should be updated."
