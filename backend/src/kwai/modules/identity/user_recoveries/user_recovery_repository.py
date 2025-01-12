"""Module that defines an interface for a user recovery repository."""

from abc import abstractmethod

from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.user_recoveries.user_recovery import UserRecoveryEntity


class UserRecoveryRepository:
    """Interface for a user recovery repository."""

    @abstractmethod
    async def get_by_uuid(self, uuid: UniqueId) -> UserRecoveryEntity:
        """Get a user recovery with the given unique id."""
        raise NotImplementedError

    @abstractmethod
    async def create(self, user_recovery: UserRecoveryEntity) -> UserRecoveryEntity:
        """Save a new user recovery."""
        raise NotImplementedError

    @abstractmethod
    async def update(self, user_recovery: UserRecoveryEntity):
        """Save a user recovery."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_recovery: UserRecoveryEntity):
        """Deletes a user recovery."""
        raise NotImplementedError


class UserRecoveryNotFoundException(Exception):
    """Raised when the user recovery could not be found."""
