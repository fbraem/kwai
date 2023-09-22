"""Module for defining the use case "Delete Page"."""
from dataclasses import dataclass

from kwai.modules.portal.pages.page import PageIdentifier
from kwai.modules.portal.pages.page_repository import PageRepository


@dataclass(kw_only=True, frozen=True, slots=True)
class DeletePageCommand:
    """Input for the use case "Delete Page"."""

    id: int


class DeletePage:
    """Use case "Delete Page"."""

    def __init__(self, repo: PageRepository):
        """Initialize the use case.

        Args:
            repo: A repository for deleting a page.
        """
        self._repo = repo

    async def execute(self, command: DeletePageCommand) -> None:
        """Executes the use case.

        Args:
            command: The input for this use case.

        Raises:
            PageNotFoundException: when the page does not exist.
        """
        page = await self._repo.get_by_id(PageIdentifier(command.id))
        await self._repo.delete(page)
