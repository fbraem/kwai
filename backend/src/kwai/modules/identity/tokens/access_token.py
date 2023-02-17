"""Module that defines an access token entity."""
from dataclasses import dataclass, field
from datetime import datetime

from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.users.user_account import UserAccountEntity

AccessTokenIdentifier = IntIdentifier


@dataclass(kw_only=True)
class AccessTokenEntity:
    """An access token entity."""

    user_account: UserAccountEntity
    id: AccessTokenIdentifier = field(default_factory=AccessTokenIdentifier)
    identifier: TokenIdentifier = field(default_factory=TokenIdentifier.generate)
    expiration: datetime = field(default_factory=datetime.utcnow)
    revoked: bool = False
    traceable_time: TraceableTime = field(default_factory=TraceableTime)

    @property
    def expired(self) -> bool:
        """Return true when the access token is expired."""
        return self.expiration < datetime.utcnow()

    def revoke(self) -> None:
        """Revoke the access token."""
        self.revoked = True
        self.traceable_time = self.traceable_time.mark_for_update()
