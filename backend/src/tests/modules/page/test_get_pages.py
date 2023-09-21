"""Module for testing the use case "Get Pages"."""

from kwai.modules.page.get_pages import GetPages, GetPagesCommand
from kwai.modules.page.pages.page import PageEntity
from kwai.modules.page.pages.page_repository import PageRepository


async def test_get_pages(repo: PageRepository, saved_page: PageEntity):
    """Test use case."""
    command = GetPagesCommand()
    result = await GetPages(repo).execute(command)
    assert result.count >= 1, "There should be a count"
    page = await anext(
        page async for page in result.iterator if page.id == saved_page.id
    )
    assert page is not None, "There should be a result"
