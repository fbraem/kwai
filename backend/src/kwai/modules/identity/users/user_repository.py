"""Module that defines the interface for a user repository."""
from abc import ABC, abstractmethod

from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.users.user import UserEntity, UserIdentifier


class UserNotFoundException(Exception):
    pass


class UserRepository(ABC):
    """A user repository interface."""

    @abstractmethod
    def get_user_by_id(self, id_: UserIdentifier) -> UserEntity:
        """Get a user using the id."""
        raise NotImplementedError

    @abstractmethod
    def get_user_by_uuid(self, uuid: UniqueId) -> UserEntity:
        """Get a user using the unique id."""
        raise NotImplementedError

    @abstractmethod
    def get_user_by_email(self, email: EmailAddress) -> UserEntity:
        """Get a user using his/her email address."""
        raise NotImplementedError

    @abstractmethod
    def update(self, user: UserEntity) -> None:
        """Updates an existing user entity."""
        raise NotImplementedError
