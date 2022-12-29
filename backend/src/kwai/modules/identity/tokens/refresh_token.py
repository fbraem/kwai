"""Module for a refresh token entity."""
from dataclasses import dataclass
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
    access_token: AccessTokenEntity
    revoked: bool = False
    traceable_time: TraceableTime = TraceableTime()


class RefreshTokenEntity(Entity[RefreshToken]):
    """An entity for a refresh token."""
