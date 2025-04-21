"""Module that defines an interface for an Author repository."""

from abc import ABC, abstractmethod

from kwai.modules.identity.users.user import UserIdentifier
from kwai.modules.portal.domain.author import AuthorEntity


class AuthorNotFoundException(Exception):
    """Raised when an author cannot be found."""


class AuthorRepository(ABC):
    """An interface for an author repository."""

    @abstractmethod
    async def get(self, id: UserIdentifier) -> AuthorEntity:
        """Get the author with the given user identifier."""
        raise NotImplementedError

    @abstractmethod
    async def create(self, author: AuthorEntity) -> AuthorEntity:
        """Save an author entity to the database."""

    @abstractmethod
    async def delete(self, author: AuthorEntity) -> None:
        """Delete an author entity from the dabase."""
