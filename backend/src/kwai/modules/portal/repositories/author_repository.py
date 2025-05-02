"""Module that defines an interface for an Author repository."""

from abc import ABC, abstractmethod
from typing import AsyncGenerator

from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.portal.domain.author import AuthorEntity, AuthorIdentifier
from kwai.modules.portal.repositories.author_query import AuthorQuery


class AuthorNotFoundException(Exception):
    """Raised when an author cannot be found."""


class AuthorRepository(ABC):
    """An interface for an author repository."""

    @abstractmethod
    def create_query(self) -> AuthorQuery:
        """Create a query for quering authors."""
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: AuthorIdentifier) -> AuthorEntity:
        """Get the author with the given user identifier."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_uuid(self, uuid: UniqueId) -> AuthorEntity:
        """Get the author that is linked to the user with the given uuid."""
        raise NotImplementedError

    @abstractmethod
    def get_all(
        self, query: AuthorQuery | None = None, limit: int = 0, offset: int = 0
    ) -> AsyncGenerator[AuthorEntity, None]:
        """Yield all authors of a given query.

        Args:
            query: The query to use for selecting the authors.
            limit: The maximum number of entities to return.
            offset: Skip the offset rows before beginning to return entities.
        """
        raise NotImplementedError

    @abstractmethod
    async def create(self, author: AuthorEntity) -> AuthorEntity:
        """Save an author entity to the database."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, author: AuthorEntity) -> None:
        """Delete an author entity from the dabase."""
        raise NotImplementedError
