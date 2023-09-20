"""Module for testing the use case "Get Pages"."""
import pytest

from kwai.core.db.database import Database
from kwai.modules.page.get_pages import GetPages, GetPagesCommand
from kwai.modules.page.pages.page_db_repository import PageDbRepository
from kwai.modules.page.pages.page_repository import PageRepository


@pytest.fixture
def repo(database: Database) -> PageRepository:
    """Fixture for a page repository."""
    return PageDbRepository(database)


async def test_get_pages(repo: PageRepository):
    """Test use case."""
    command = GetPagesCommand()
    result = await GetPages(repo).execute(command)
    assert result.count >= 0, "There should be a count"
    pages = {page.id: page async for page in result.iterator}
    assert pages, "There should be a result"
