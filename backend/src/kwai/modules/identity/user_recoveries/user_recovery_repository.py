"""Module that defines an interface for a user recovery repository."""
from abc import abstractmethod

from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.user_recoveries import UserRecovery, UserRecoveryEntity


class UserRecoveryRepository:
    """Interface for a user recovery repository."""

    @abstractmethod
    def get_by_uuid(self, uuid: UniqueId) -> UserRecoveryEntity:
        """Get a user recovery with the given unique id."""
        raise NotImplementedError

    @abstractmethod
    def create(self, user_recovery: UserRecovery) -> UserRecoveryEntity:
        """Save a new user recovery."""
        raise NotImplementedError

    @abstractmethod
    def update(self, user_recovery: UserRecoveryEntity):
        """Save a user recovery."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_recovery: UserRecoveryEntity):
        """Deletes a user recovery."""
        raise NotImplementedError


class UserRecoveryNotFoundException(Exception):
    """Raised when the user recovery could not be found."""
