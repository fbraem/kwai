"""Module that defines an interface for an access token repository."""
from abc import abstractmethod
from typing import Iterator

from kwai.modules.identity.tokens.access_token import (
    AccessTokenEntity,
    AccessTokenIdentifier,
)
from kwai.modules.identity.tokens.access_token_query import AccessTokenQuery
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier


class AccessTokenNotFoundException(Exception):
    """Raised when the access token could not be found."""


class AccessTokenRepository:
    """Interface for an access token repository."""

    @abstractmethod
    def create_query(self) -> AccessTokenQuery:
        """Create a query for a access token."""
        raise NotImplementedError

    @abstractmethod
    async def create(self, access_token: AccessTokenEntity) -> AccessTokenEntity:
        """Save a new access token."""
        raise NotImplementedError

    @abstractmethod
    async def update(self, access_token: AccessTokenEntity):
        """Update the access token."""
        raise NotImplementedError

    @abstractmethod
    async def get(self, id_: AccessTokenIdentifier) -> AccessTokenEntity:
        """Get the access token with the given id."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_identifier(self, identifier: TokenIdentifier) -> AccessTokenEntity:
        """Get the access token with the given identifier."""
        raise NotImplementedError

    @abstractmethod
    async def get_all(
        self,
        query: AccessTokenQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Iterator[AccessTokenEntity]:
        """Get all access token."""
        raise NotImplementedError
