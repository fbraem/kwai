"""Module for a refresh token entity."""
from dataclasses import dataclass, field
from datetime import datetime

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.modules.identity.tokens.access_token import AccessTokenEntity
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier


@dataclass(kw_only=True)
class RefreshToken:
    """A refresh token domain object."""

    identifier: TokenIdentifier
    expiration: datetime
    is_expired: bool = field(init=False)
    access_token: AccessTokenEntity
    revoked: bool = False
    traceable_time: TraceableTime = TraceableTime()

    def __post_init__(self):
        self.is_expired = self.expiration < datetime.utcnow()

    def revoke(self):
        """Revoke the refresh token."""
        self.revoked = True


class RefreshTokenEntity(Entity[RefreshToken]):
    """An entity for a refresh token."""
