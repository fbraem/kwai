"""Module that defines all tables for tokens."""

from dataclasses import dataclass
from datetime import datetime
from typing import Self

from kwai.core.db.table_row import TableRow, unwrap
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
from kwai.modules.identity.tokens.user_log import UserLogEntity, UserLogIdentifier
from kwai.modules.identity.tokens.value_objects import IpAddress, OpenId
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
            id=AccessTokenIdentifier(unwrap(self.id)),
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
            expiration=unwrap(access_token.expiration.timestamp),
            user_id=access_token.user_account.id.value,
            revoked=1 if access_token.revoked else 0,
            created_at=unwrap(access_token.traceable_time.created_at.timestamp),
            updated_at=access_token.traceable_time.updated_at.timestamp,
        )


@dataclass(kw_only=True, frozen=True, slots=True)
class RefreshTokenRow(TableRow):
    """Represent a table row in the refresh token table."""

    __table_name__ = "oauth_refresh_tokens"

    id: int | None = None
    identifier: str
    access_token_id: int
    expiration: datetime
    revoked: int
    created_at: datetime
    updated_at: datetime | None

    def create_entity(self, access_token: AccessTokenEntity) -> RefreshTokenEntity:
        """Create a refresh token entity from the table row."""
        return RefreshTokenEntity(
            id=RefreshTokenIdentifier(unwrap(self.id)),
            identifier=TokenIdentifier(hex_string=self.identifier),
            access_token=access_token,
            expiration=Timestamp.create_utc(self.expiration),
            revoked=self.revoked == 1,
            traceable_time=TraceableTime(
                created_at=unwrap(Timestamp.create_utc(self.created_at)),
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
            expiration=unwrap(refresh_token.expiration.timestamp),
            revoked=1 if refresh_token.revoked else 0,
            created_at=unwrap(refresh_token.traceable_time.created_at.timestamp),
            updated_at=refresh_token.traceable_time.updated_at.timestamp,
        )


@dataclass(kw_only=True, frozen=True, slots=True)
class UserLogRow(TableRow):
    """Represent a table row in the user logs table."""

    __table_name__ = "user_logs"

    id: int
    success: int
    email: str
    refresh_token_id: int | None
    client_ip: str
    user_agent: str
    openid_sub: str
    openid_provider: str
    remark: str
    created_at: datetime

    def create_entity(self, refresh_token: RefreshTokenEntity | None) -> UserLogEntity:
        """Create a User Log entity from the table row."""
        return UserLogEntity(
            id=UserLogIdentifier(self.id),
            email=self.email,
            refresh_token=refresh_token,
            client_ip=IpAddress.create(self.client_ip),
            user_agent=self.user_agent,
            remark=self.remark,
            openid=OpenId(sub=self.openid_sub, provider=self.openid_provider),
            created_at=Timestamp.create_utc(self.created_at),
        )

    @classmethod
    def persist(cls, user_log: UserLogEntity) -> Self:
        """Transform a user log entity into a table record."""
        return cls(
            id=user_log.id.value,
            success=1 if user_log.success else 0,
            email=user_log.email,
            refresh_token_id=None
            if user_log.refresh_token is None
            else user_log.refresh_token.id.value,
            client_ip=str(user_log.client_ip),
            user_agent=user_log.user_agent,
            openid_sub=user_log.openid.sub,
            openid_provider=user_log.openid.provider,
            remark=user_log.remark,
            created_at=unwrap(user_log.created_at.timestamp),
        )
