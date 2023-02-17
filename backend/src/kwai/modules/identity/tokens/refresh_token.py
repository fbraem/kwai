"""Module for a refresh token entity."""
from dataclasses import dataclass, field
from datetime import datetime

from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.modules.identity.tokens.access_token import AccessTokenEntity
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier

RefreshTokenIdentifier = IntIdentifier


@dataclass(kw_only=True)
class RefreshTokenEntity:
    """A refresh token entity."""

    access_token: AccessTokenEntity
    id: RefreshTokenIdentifier = field(default_factory=RefreshTokenIdentifier)
    identifier: TokenIdentifier = field(default_factory=TokenIdentifier.generate)
    expiration: datetime = field(default_factory=datetime.utcnow)
    revoked: bool = False
    traceable_time: TraceableTime = field(default_factory=TraceableTime)

    @property
    def expired(self) -> bool:
        """Return True when the token is expired."""
        return self.expiration < datetime.utcnow()

    def revoke(self) -> None:
        """Revoke the refresh token."""
        self.revoked = True
        self.access_token.revoke()
        self.traceable_time = self.traceable_time.mark_for_update()
