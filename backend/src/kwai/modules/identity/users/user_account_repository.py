"""Module that defines a repository for a user account."""
from abc import abstractmethod

from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.modules.identity.users.user_account import UserAccountEntity


class UserAccountRepository:
    """Interface for a user account repository."""

    @abstractmethod
    def get_user_by_email(self, email: EmailAddress) -> UserAccountEntity:
        """Get a user account with the given email address."""
        raise NotImplementedError

    @abstractmethod
    def create(self, user_account: UserAccountEntity) -> UserAccountEntity:
        """Save a new user account."""
        raise NotImplementedError

    @abstractmethod
    def update(self, user_account_entity: UserAccountEntity):
        """Save a user account."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_account_entity):
        """Deletes a user account."""
        raise NotImplementedError


class UserAccountNotFoundException(Exception):
    """Raised when a user account cannot be found."""
