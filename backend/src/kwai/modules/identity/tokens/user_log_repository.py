"""Module that defines an interface for a UserLog repository."""

from abc import ABC, abstractmethod

from kwai.modules.identity.tokens.user_log import UserLogEntity


class UserLogRepository(ABC):
    """Interface for UserLog repository."""

    @abstractmethod
    async def create(self, user_log: UserLogEntity) -> UserLogEntity:
        """Create a new UserLog entity."""
