"""Module that defines an interface for a service that logs a user login request."""

from abc import ABC, abstractmethod

from kwai.modules.identity.tokens.refresh_token import RefreshTokenEntity
from kwai.modules.identity.users.user_account import UserAccountEntity


class LogUserLoginService(ABC):
    """Abstract interface for a service that logs a user login request."""

    @abstractmethod
    async def notify_failure(
        self,
        message: str = "",
        *,
        user_account: UserAccountEntity | None = None,
        refresh_token: RefreshTokenEntity | None = None,
    ) -> None:
        """Register a failed user login request."""
        raise NotImplementedError()

    @abstractmethod
    async def notify_success(
        self,
        *,
        user_account: UserAccountEntity | None = None,
        refresh_token: RefreshTokenEntity | None = None,
    ) -> None:
        """Register a successful user login request."""
        raise NotImplementedError()
