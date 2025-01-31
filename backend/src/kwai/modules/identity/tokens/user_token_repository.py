"""Module for defining an interface for a user token repository."""

from abc import ABC, abstractmethod

from kwai.modules.identity.users.user_account import UserAccountEntity


class UserTokenRepository(ABC):
    """An interface for a user token repository.

    This repository is responsible for processing tokens of a specific user.
    """

    @abstractmethod
    async def revoke(self, user_account: UserAccountEntity):
        """Revoke all access and refresh tokens for the user."""
        raise NotImplementedError()
