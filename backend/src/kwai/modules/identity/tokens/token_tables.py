"""Module that defines all tables for tokens."""
from dataclasses import dataclass
from datetime import datetime

from kwai.core.db.table import table
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.modules.identity.tokens.access_token import (
    AccessTokenEntity,
    AccessTokenIdentifier,
)
from kwai.modules.identity.tokens.refresh_token import (
    RefreshTokenEntity,
    RefreshTokenIdentifier,
)
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.users.user_account import UserAccountEntity


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

    def create_entity(self, user_account: UserAccountEntity) -> AccessTokenEntity:
        """Create an entity from the table row."""
        return AccessTokenEntity(
            id=AccessTokenIdentifier(self.id),
            identifier=TokenIdentifier(self.identifier),
            expiration=self.expiration,
            user_account=user_account,
            revoked=self.revoked,
            traceable_time=TraceableTime(
                created_at=self.created_at,
                updated_at=self.updated_at,
            ),
        )

    @classmethod
    def persist(cls, access_token: AccessTokenEntity) -> "AccessTokensTable":
        """Persist an access token entity to a table record."""
        return AccessTokensTable(
            id=access_token.id.value,
            identifier=str(access_token.identifier),
            expiration=access_token.expiration,
            user_id=access_token.user_account.id.value,
            revoked=access_token.revoked,
            created_at=access_token.traceable_time.created_at,
            updated_at=access_token.traceable_time.updated_at,
        )


@table(name="oauth_refresh_tokens")
@dataclass(kw_only=True, frozen=True, slots=True)
class RefreshTokensTable:
    """Table for refresh tokens."""

    id: int | None
    identifier: str
    access_token_id: int
    expiration: datetime
    revoked: bool
    created_at: datetime
    updated_at: datetime

    def create_entity(self, access_token: AccessTokenEntity) -> RefreshTokenEntity:
        """Create a refresh token entity from the table row."""
        return RefreshTokenEntity(
            id=RefreshTokenIdentifier(self.id),
            identifier=TokenIdentifier(self.identifier),
            access_token=access_token,
            expiration=self.expiration,
            revoked=self.revoked,
            traceable_time=TraceableTime(
                created_at=self.created_at,
                updated_at=self.updated_at,
            ),
        )

    @classmethod
    def persist(cls, refresh_token: RefreshTokenEntity) -> "RefreshTokensTable":
        """Transform a refresh token entity into a table record."""
        return RefreshTokensTable(
            id=refresh_token.id.value,
            identifier=str(refresh_token.identifier),
            access_token_id=refresh_token.access_token.id.value,
            expiration=refresh_token.expiration,
            revoked=refresh_token.revoked,
            created_at=refresh_token.traceable_time.created_at,
            updated_at=refresh_token.traceable_time.updated_at,
        )
