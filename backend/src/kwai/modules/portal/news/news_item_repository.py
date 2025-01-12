"""Module that defines an interface for a news item repository."""

from abc import ABC, abstractmethod
from typing import AsyncIterator

from kwai.modules.portal.news.news_item import NewsItemEntity, NewsItemIdentifier
from kwai.modules.portal.news.news_item_query import NewsItemQuery


class NewsItemNotFoundException(Exception):
    """Raised when the news item can not be found."""


class NewsItemRepository(ABC):
    """Interface for a news item repository."""

    @abstractmethod
    async def create(self, news_item: NewsItemEntity) -> NewsItemEntity:
        """Create a new news item entity.

        Args:
            news_item: The news item to create

        Returns:
            The news item entity with an identifier.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, news_item: NewsItemEntity):
        """Update a news item entity.

        Args:
            news_item: The news item to update.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, news_item: NewsItemEntity):
        """Delete a news item.

        Args:
            news_item: The news item to delete.
        """
        raise NotImplementedError

    @abstractmethod
    def create_query(self) -> NewsItemQuery:
        """Create a query for querying news items."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id_: NewsItemIdentifier) -> NewsItemEntity:
        """Get the news item with the given id.

        Args:
            id_: The id of the news item.

        Returns:
            A news item entity.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all(
        self,
        query: NewsItemQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncIterator[NewsItemEntity]:
        """Return all news items of a given query.

        Args:
            query: The query to use for selecting the rows.
            limit: The maximum number of entities to return.
            offset: Skip the offset rows before beginning to return entities.

        Yields:
            A list of news items.
        """
        raise NotImplementedError
