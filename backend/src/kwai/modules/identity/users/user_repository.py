"""Module that defines the interface for a user repository."""

from abc import ABC, abstractmethod

from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.users.user import UserEntity, UserIdentifier


class UserNotFoundException(Exception):
    """Raised when a user could not be found."""


class UserRepository(ABC):
    """A user repository interface."""

    @abstractmethod
    async def get_user_by_id(self, id_: UserIdentifier) -> UserEntity:
        """Get a user using the id."""
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_uuid(self, uuid: UniqueId) -> UserEntity:
        """Get a user using the unique id."""
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_email(self, email: EmailAddress) -> UserEntity:
        """Get a user using his/her email address."""
        raise NotImplementedError

    @abstractmethod
    async def update(self, user: UserEntity) -> None:
        """Update an existing user entity."""
        raise NotImplementedError
