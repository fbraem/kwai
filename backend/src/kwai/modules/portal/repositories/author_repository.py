"""Module that defines an interface for an Author repository."""

from abc import ABC, abstractmethod

from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.portal.domain.author import AuthorEntity, AuthorIdentifier


class AuthorNotFoundException(Exception):
    """Raised when an author cannot be found."""


class AuthorRepository(ABC):
    """An interface for an author repository."""

    @abstractmethod
    async def get(self, id: AuthorIdentifier) -> AuthorEntity:
        """Get the author with the given user identifier."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_uuid(self, uuid: UniqueId) -> AuthorEntity:
        """Get the author that is linked to the user with the given uuid."""
        raise NotImplementedError

    @abstractmethod
    async def create(self, author: AuthorEntity) -> AuthorEntity:
        """Save an author entity to the database."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, author: AuthorEntity) -> None:
        """Delete an author entity from the dabase."""
        raise NotImplementedError
