"""Module that defines an access token entity."""
from datetime import datetime
from dataclasses import dataclass, field

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.users import UserAccountEntity


@dataclass(kw_only=True)
class AccessToken:
    """An access token domain object."""

    identifier: TokenIdentifier
    expiration: datetime
    is_expired: bool = field(init=False)
    user_account: UserAccountEntity
    revoked: bool = False
    traceable_time: TraceableTime = TraceableTime()

    def __post_init__(self):
        self.is_expired = self.expiration < datetime.utcnow()

    def revoke(self):
        """Revoke the access token."""
        self.revoked = True


class AccessTokenEntity(Entity[AccessToken]):
    """An entity for an access token domain object."""
