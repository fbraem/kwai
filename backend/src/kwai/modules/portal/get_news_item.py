"""Module for the use case "Get News Item"."""
from dataclasses import dataclass

from kwai.modules.portal.news.news_item import NewsItemEntity, NewsItemIdentifier
from kwai.modules.portal.news.news_item_repository import NewsItemRepository


@dataclass(kw_only=True, frozen=True, slots=True)
class GetNewsItemCommand:
    """Input for the use case "Get News Item"."""

    id: int


class GetNewsItem:
    """Use case "Get News Item"."""

    def __init__(self, repo: NewsItemRepository):
        """Initialize the use case.

        Args:
            repo: A repository for getting the news item.
        """
        self._repo = repo

    async def execute(self, command: GetNewsItemCommand) -> NewsItemEntity:
        """Executes the use case.

        Args:
            command: The input for this use case.

        Returns: A news item entity.

        Raises:
            NewsItemNotFoundException: When the news item does not exist.
        """
        return await self._repo.get_by_id(NewsItemIdentifier(command.id))
