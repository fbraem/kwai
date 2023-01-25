"""Module that defines an interface for an access token query."""
from abc import abstractmethod

from kwai.core.domain.repository.query import Query
from .token_identifier import TokenIdentifier


class AccessTokenQuery(Query):
    """An interface for querying an access token."""

    @abstractmethod
    def filter_by_id(self, id_: int) -> "AccessTokenQuery":
        """Filter for the given id."""
        raise NotImplementedError

    @abstractmethod
    def filter_by_token_identifier(
        self, identifier: TokenIdentifier
    ) -> "AccessTokenQuery":
        """Filter for the given token identifier."""
        raise NotImplementedError
