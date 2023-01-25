"""Module that defines an interface for querying a refresh token."""
from abc import abstractmethod

from kwai.core.domain.repository.query import Query
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier


class RefreshTokenQuery(Query):
    """An interface for querying a refresh token."""

    @abstractmethod
    def filter_by_id(self, id_: int) -> "RefreshTokenQuery":
        """Filter for the given id."""
        raise NotImplementedError

    @abstractmethod
    def filter_by_token_identifier(
        self, identifier: TokenIdentifier
    ) -> "RefreshTokenQuery":
        """Filter for the given token identifier."""
        raise NotImplementedError
