"""Module for defining the use case "Delete News Item"."""
from dataclasses import dataclass

from kwai.modules.portal.news.news_item import NewsItemIdentifier
from kwai.modules.portal.news.news_item_repository import NewsItemRepository


@dataclass(kw_only=True, frozen=True, slots=True)
class DeleteNewsItemCommand:
    """Input for the use case "Delete News Item"."""

    id: int


class DeleteNewsItem:
    """Use case "Delete Page"."""

    def __init__(self, repo: NewsItemRepository):
        """Initialize the use case.

        Args:
            repo: A repository for deleting a news item.
        """
        self._repo = repo

    async def execute(self, command: DeleteNewsItemCommand) -> None:
        """Executes the use case.

        Args:
            command: The input for this use case.

        Raises:
            NewsItemNotFoundException: when the news item does not exist.
        """
        news_item = await self._repo.get_by_id(NewsItemIdentifier(command.id))
        await self._repo.delete(news_item)
