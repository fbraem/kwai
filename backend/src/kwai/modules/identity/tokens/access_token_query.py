"""Module that defines an interface for an access token query."""

from abc import abstractmethod
from typing import Self

from kwai.core.domain.repository.query import Query
from kwai.modules.identity.tokens.access_token import AccessTokenIdentifier
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.users.user_account import UserAccountEntity


class AccessTokenQuery(Query):
    """An interface for querying an access token."""

    @abstractmethod
    def filter_by_id(self, id_: AccessTokenIdentifier) -> Self:
        """Filter for the given id."""
        raise NotImplementedError

    @abstractmethod
    def filter_by_token_identifier(self, identifier: TokenIdentifier) -> Self:
        """Filter for the given token identifier."""
        raise NotImplementedError

    @abstractmethod
    def filter_by_user_account(self, user_account: UserAccountEntity) -> Self:
        """Filter for the given user account."""
        raise NotImplementedError
