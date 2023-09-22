"""Module for the use case "Get Story"."""
from dataclasses import dataclass

from kwai.modules.portal.news.news_item import NewsItemEntity, NewsItemIdentifier
from kwai.modules.portal.news.news_item_repository import NewsItemRepository


@dataclass(kw_only=True, frozen=True, slots=True)
class GetStoryCommand:
    """Input for the use case "Get Story"."""

    id: int


class GetStory:
    """Use case "Get Story"."""

    def __init__(self, repo: NewsItemRepository):
        """Initialize the use case.

        Args:
            repo: A repository for getting the news story.
        """
        self._repo = repo

    async def execute(self, command: GetStoryCommand) -> NewsItemEntity:
        """Executes the use case.

        Args:
            command: The input for this use case.

        Returns: A story entity.

        Raises:
            StoryNotFoundException: When the story does not exist.
        """
        return await self._repo.get_by_id(NewsItemIdentifier(command.id))
