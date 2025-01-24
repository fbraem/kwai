"""Module that defines a repository for a user account."""

from abc import abstractmethod
from collections.abc import AsyncGenerator

from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.modules.identity.users.user_account import UserAccountEntity


class UserAccountRepository:
    """Interface for a user account repository."""

    @abstractmethod
    async def get_all(
        self, limit: int | None = None, offset: int | None = None
    ) -> AsyncGenerator[UserAccountEntity]:
        """Return all user accounts.

        Args:
            limit: The maximum number of entities to return.
            offset: Skip the offset rows before beginning to return entities.

        Yields:
            A list of user account entities.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_email(self, email: EmailAddress) -> UserAccountEntity:
        """Get a user account with the given email address."""
        raise NotImplementedError

    async def exists_with_email(self, email: EmailAddress) -> bool:
        """Check if a user account with the given email address already exists.

        Args:
            email: The email address to check.

        Returns:
            True when a user with the given email address exists.
        """
        raise NotImplementedError

    @abstractmethod
    async def create(self, user_account: UserAccountEntity) -> UserAccountEntity:
        """Save a new user account."""
        raise NotImplementedError

    @abstractmethod
    async def update(self, user_account: UserAccountEntity):
        """Save a user account."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_account):
        """Delete a user account."""
        raise NotImplementedError


class UserAccountNotFoundException(Exception):
    """Raised when a user account cannot be found."""
