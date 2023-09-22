"""Module for testing the use case "Delete Page"."""
import pytest

from kwai.modules.portal.delete_page import DeletePage, DeletePageCommand
from kwai.modules.portal.get_page import GetPage, GetPageCommand
from kwai.modules.portal.pages.page import PageEntity
from kwai.modules.portal.pages.page_repository import (
    PageNotFoundException,
    PageRepository,
)


async def test_delete_page(page_repo: PageRepository, saved_page: PageEntity):
    """Test delete page."""
    command = DeletePageCommand(id=saved_page.id.value)
    await DeletePage(page_repo).execute(command)

    command = GetPageCommand(id=saved_page.id.value)
    with pytest.raises(PageNotFoundException):
        await GetPage(page_repo).execute(command)
