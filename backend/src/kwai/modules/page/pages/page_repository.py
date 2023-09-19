"""Module that defines an interface for a page repository."""
from abc import ABC, abstractmethod
from typing import AsyncIterator

from kwai.modules.page.pages.page import PageEntity, PageIdentifier
from kwai.modules.page.pages.page_query import PageQuery


class PageNotFoundException(Exception):
    """Raised when a page can not be found."""


class PageRepository(ABC):
    """Interface for a page repository."""

    @abstractmethod
    async def create(self, page: PageEntity) -> PageEntity:
        """Create a new page entity.

        Args:
            page: The page to create.

        Returns:
            The page entity with an identifier.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, page: PageEntity):
        """Update a page entity.

        Args:
            page: The page to update.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, page: PageEntity):
        """Delete a page.

        Args:
            page: The page to delete.
        """
        raise NotImplementedError

    @abstractmethod
    def create_query(self) -> PageQuery:
        """Create a query for querying pages."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id_: PageIdentifier) -> PageEntity:
        """Get the page with the given id.

        Args:
            id_: The id of the page.

        Returns:
            A page entity.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all(
        self,
        query: PageQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncIterator[PageEntity]:
        """Return all pages of a given query.

        Args:
            query: The query to use for selecting the rows.
            limit: The maximum number of entities to return.
            offset: Skip the offset rows before beginning to return entities.

        Yields:
            A list of pages.
        """
        raise NotImplementedError
