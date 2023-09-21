"""Module for the use case "Get Page"."""
from dataclasses import dataclass

from kwai.modules.page.pages.page import PageEntity, PageIdentifier
from kwai.modules.page.pages.page_repository import PageRepository


@dataclass(kw_only=True, frozen=True, slots=True)
class GetPageCommand:
    """Input for the use case "Get Page"."""

    id: int


class GetPage:
    """Use case "Get Page"."""

    def __init__(self, repo: PageRepository):
        """Initialize the use case.

        Args:
            repo: A repository to get the page.
        """
        self._repo = repo

    async def execute(self, command: GetPageCommand) -> PageEntity:
        """Execute the use case."""
        return await self._repo.get_by_id(PageIdentifier(command.id))
