"""Module that defines an interface for querying a refresh token."""

from abc import abstractmethod
from typing import Self

from kwai.core.domain.repository.query import Query
from kwai.modules.identity.tokens.refresh_token import RefreshTokenIdentifier
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.users.user_account import UserAccountEntity


class RefreshTokenQuery(Query):
    """An interface for querying a refresh token."""

    @abstractmethod
    def filter_by_id(self, id_: RefreshTokenIdentifier) -> "RefreshTokenQuery":
        """Filter for the given id."""
        raise NotImplementedError

    @abstractmethod
    def filter_by_token_identifier(
        self, identifier: TokenIdentifier
    ) -> "RefreshTokenQuery":
        """Filter for the given token identifier."""
        raise NotImplementedError

    @abstractmethod
    def filter_by_user_account(self, user_account: UserAccountEntity) -> Self:
        """Filter for the given user account."""
        raise NotImplementedError
