"""Module that defines all tables for tokens."""

from dataclasses import dataclass
from datetime import datetime

from kwai.core.db.table_row import TableRow
from kwai.core.domain.value_objects.timestamp import Timestamp
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


@dataclass(kw_only=True, frozen=True, slots=True)
class AccessTokenRow(TableRow):
    """Represent a table row in the access tokens table."""

    __table_name__ = "oauth_access_tokens"

    id: int | None
    identifier: str
    expiration: datetime
    user_id: int
    revoked: int
    created_at: datetime
    updated_at: datetime | None

    def create_entity(self, user_account: UserAccountEntity) -> AccessTokenEntity:
        """Create an entity from the table row."""
        return AccessTokenEntity(
            id=AccessTokenIdentifier(self.id),
            identifier=TokenIdentifier(hex_string=self.identifier),
            expiration=Timestamp.create_utc(self.expiration),
            user_account=user_account,
            revoked=self.revoked == 1,
            traceable_time=TraceableTime(
                created_at=Timestamp.create_utc(self.created_at),
                updated_at=Timestamp.create_utc(self.updated_at),
            ),
        )

    @classmethod
    def persist(cls, access_token: AccessTokenEntity) -> "AccessTokenRow":
        """Persist an access token entity to a table record."""
        return AccessTokenRow(
            id=access_token.id.value,
            identifier=str(access_token.identifier),
            expiration=access_token.expiration.timestamp,
            user_id=access_token.user_account.id.value,
            revoked=access_token.revoked,
            created_at=access_token.traceable_time.created_at.timestamp,
            updated_at=access_token.traceable_time.updated_at.timestamp,
        )


@dataclass(kw_only=True, frozen=True, slots=True)
class RefreshTokenRow(TableRow):
    """Represent a table row in the refresh token table."""

    __table_name__ = "oauth_refresh_tokens"

    id: int | None
    identifier: str
    access_token_id: int
    expiration: datetime
    revoked: int
    created_at: datetime
    updated_at: datetime | None

    def create_entity(self, access_token: AccessTokenEntity) -> RefreshTokenEntity:
        """Create a refresh token entity from the table row."""
        return RefreshTokenEntity(
            id=RefreshTokenIdentifier(self.id),
            identifier=TokenIdentifier(hex_string=self.identifier),
            access_token=access_token,
            expiration=Timestamp.create_utc(self.expiration),
            revoked=self.revoked == 1,
            traceable_time=TraceableTime(
                created_at=Timestamp.create_utc(self.created_at),
                updated_at=Timestamp.create_utc(self.updated_at),
            ),
        )

    @classmethod
    def persist(cls, refresh_token: RefreshTokenEntity) -> "RefreshTokenRow":
        """Transform a refresh token entity into a table record."""
        return RefreshTokenRow(
            id=refresh_token.id.value,
            identifier=str(refresh_token.identifier),
            access_token_id=refresh_token.access_token.id.value,
            expiration=refresh_token.expiration.timestamp,
            revoked=refresh_token.revoked,
            created_at=refresh_token.traceable_time.created_at.timestamp,
            updated_at=refresh_token.traceable_time.updated_at.timestamp,
        )
