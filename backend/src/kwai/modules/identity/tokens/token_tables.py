"""Module that defines all tables for tokens."""
from dataclasses import dataclass
from datetime import datetime

from kwai.core.db import table
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.modules.identity.tokens.access_token import (
    AccessTokenEntity,
    AccessTokenIdentifier,
)
from kwai.modules.identity.tokens.refresh_token import RefreshToken, RefreshTokenEntity
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.users.user_tables import UserAccountMapper


@table(name="oauth_access_tokens")
@dataclass(kw_only=True, frozen=True, slots=True)
class AccessTokensTable:
    """Table for access tokens."""

    id: int | None
    identifier: str
    expiration: datetime
    user_id: int
    revoked: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def persist(cls, access_token: AccessTokenEntity) -> "AccessTokensTable":
        return AccessTokensTable(
            id=access_token.id.value,
            identifier=str(access_token.identifier),
            expiration=access_token.expiration,
            user_id=access_token.user_account.id,
            revoked=access_token.revoked,
            created_at=access_token.traceable_time.created_at,
            updated_at=access_token.traceable_time.updated_at,
        )


@dataclass(kw_only=True, frozen=True)
class AccessTokenMapper:
    """Transforms a row into an access token entity."""

    access_token_table: AccessTokensTable
    user_account_mapper: UserAccountMapper

    def create_entity(self) -> AccessTokenEntity:
        """Creates an access token entity from a table row"""
        return AccessTokenEntity(
            id=AccessTokenIdentifier(self.access_token_table.id),
            identifier=TokenIdentifier(self.access_token_table.identifier),
            expiration=self.access_token_table.expiration,
            user_account=self.user_account_mapper.create_entity(),
            revoked=self.access_token_table.revoked,
            traceable_time=TraceableTime(
                created_at=self.access_token_table.created_at,
                updated_at=self.access_token_table.updated_at,
            ),
        )


@table(name="oauth_refresh_tokens")
@dataclass(kw_only=True, frozen=True, slots=True)
class RefreshTokensTable:
    id: int | None
    identifier: str
    access_token_id: int
    expiration: datetime
    revoked: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def persist(cls, refresh_token: RefreshToken) -> "RefreshTokensTable":
        return RefreshTokensTable(
            id=None,
            identifier=str(refresh_token.identifier),
            access_token_id=refresh_token.access_token.id.value,
            expiration=refresh_token.expiration,
            revoked=refresh_token.revoked,
            created_at=refresh_token.traceable_time.created_at,
            updated_at=refresh_token.traceable_time.updated_at,
        )

    @classmethod
    def persist_entity(cls, refresh_token: RefreshTokenEntity) -> "RefreshTokensTable":
        return cls.persist(refresh_token()).replace(id=refresh_token.id)


@dataclass(kw_only=True, frozen=True)
class RefreshTokenMapper:
    refresh_token_table: RefreshTokensTable
    access_token_mapper: AccessTokenMapper

    def create_entity(self) -> RefreshTokenEntity:
        return RefreshTokenEntity(
            id=self.refresh_token_table.id,
            domain=RefreshToken(
                identifier=TokenIdentifier(self.refresh_token_table.identifier),
                access_token=self.access_token_mapper.create_entity(),
                expiration=self.refresh_token_table.expiration,
                revoked=self.refresh_token_table.revoked,
                traceable_time=TraceableTime(
                    created_at=self.refresh_token_table.created_at,
                    updated_at=self.refresh_token_table.updated_at,
                ),
            ),
        )
