"""Module that defines an interface for an application repository."""
from abc import ABC, abstractmethod
from typing import AsyncIterator

from kwai.modules.portal.applications.application import (
    ApplicationEntity,
    ApplicationIdentifier,
)
from kwai.modules.portal.applications.application_query import ApplicationQuery


class ApplicationNotFoundException(Exception):
    """Raised when the application can not be found."""


class ApplicationRepository(ABC):
    """An application repository interface."""

    @abstractmethod
    def create_query(self) -> ApplicationQuery:
        """Create a query for querying applications."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id_: ApplicationIdentifier) -> ApplicationEntity:
        """Get the application with the given id.

        Args:
            id_: The id of the application.

        Returns:
            An application entity.

        Raises:
            ApplicationNotFoundException: when the application does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: str) -> ApplicationEntity:
        """Get the application with the given name.

        Args:
            name: The name of the application.

        Returns:
            An application entity.

        Raises:
            ApplicationNotFoundException: when the application with the given name
                does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all(
        self,
        query: ApplicationQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncIterator[ApplicationEntity]:
        """Return all applications of a given query.

        Args:
            query: The query to use for selecting the rows.
            limit: The maximum number of entities to return.
            offset: Skip the offset rows before beginning to return entities.

        Yields:
            A list of applications.
        """
        raise NotImplementedError

    @abstractmethod
    async def create(self, application: ApplicationEntity) -> ApplicationEntity:
        """Create a new application entity.

        Args:
            application: The application to create.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, application: ApplicationEntity):
        """Update an application entity.

        Args:
            application: The application to update.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, application: ApplicationEntity):
        """Delete an application entity.

        Args:
            application: The application to delete.
        """
        raise NotImplementedError
