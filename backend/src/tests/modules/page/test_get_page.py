"""Module for testing the use case "Get Page"."""
from kwai.modules.page.get_page import GetPage, GetPageCommand
from kwai.modules.page.pages.page import PageEntity
from kwai.modules.page.pages.page_repository import PageRepository


async def test_get_page(repo: PageRepository, saved_page: PageEntity):
    """Test the "Get Page" use case."""
    command = GetPageCommand(id=saved_page.id.value)
    page = await GetPage(repo).execute(command)
    assert page is not None, "There should be a page."
    assert page.id == saved_page.id, "The id of the pages should be the same."
