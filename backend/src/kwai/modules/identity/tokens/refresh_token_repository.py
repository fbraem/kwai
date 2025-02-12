"""Module that defines an interface for a refresh token repository."""

from abc import ABC, abstractmethod
from typing import AsyncIterator

from kwai.modules.identity.tokens.refresh_token import (
    RefreshTokenEntity,
    RefreshTokenIdentifier,
)
from kwai.modules.identity.tokens.refresh_token_query import RefreshTokenQuery
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier


class RefreshTokenNotFoundException(Exception):
    """Raised when the refresh token can't be found."""


class RefreshTokenRepository(ABC):
    """Interface for a refresh token repository."""

    @abstractmethod
    def create_query(self) -> RefreshTokenQuery:
        """Create a query for a refresh token."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_token_identifier(
        self, identifier: TokenIdentifier
    ) -> RefreshTokenEntity:
        """Get the refresh token with the given token identifier."""
        raise NotImplementedError

    @abstractmethod
    async def get(self, id_: RefreshTokenIdentifier) -> RefreshTokenEntity:
        """Get the refresh token entity with the given id."""
        raise NotImplementedError

    @abstractmethod
    def get_all(
        self,
        query: RefreshTokenQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncIterator[RefreshTokenEntity]:
        """Get all refresh tokens."""
        raise NotImplementedError

    @abstractmethod
    async def create(self, refresh_token: RefreshTokenEntity) -> RefreshTokenEntity:
        """Save a new refresh token."""
        raise NotImplementedError

    @abstractmethod
    async def update(self, refresh_token: RefreshTokenEntity):
        """Update the refresh token."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, refresh_token: RefreshTokenEntity):
        """Delete the refresh token."""
        raise NotImplementedError
