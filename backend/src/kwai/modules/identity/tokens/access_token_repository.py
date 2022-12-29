"""Module that defines an interface for an access token repository."""
from abc import abstractmethod
from typing import Iterator

from kwai.modules.identity.tokens import AccessTokenQuery, TokenIdentifier
from kwai.modules.identity.tokens.access_token import AccessToken, AccessTokenEntity


class AccessTokenNotFoundException(Exception):
    """Raised when the access token could not be found."""


class AccessTokenRepository:
    """Interface for an access token repository."""

    @abstractmethod
    def create_query(self) -> AccessTokenQuery:
        """Create a query for a access token."""
        raise NotImplementedError

    @abstractmethod
    def create(self, access_token: AccessToken) -> AccessTokenEntity:
        """Save a new access token."""
        raise NotImplementedError

    @abstractmethod
    def update(self, access_token: AccessToken):
        """Update the access token."""
        raise NotImplementedError

    @abstractmethod
    def get(self, id_: int) -> AccessTokenEntity:
        """Get the access token with the given id."""
        raise NotImplementedError

    @abstractmethod
    def get_by_identifier(self, identifier: TokenIdentifier) -> AccessTokenEntity:
        """Get the access token with the given identifier."""
        raise NotImplementedError

    @abstractmethod
    def get_all(
        self,
        query: AccessTokenQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Iterator[AccessTokenEntity]:
        """Get all access token."""
        raise NotImplementedError
