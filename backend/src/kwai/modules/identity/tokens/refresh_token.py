"""Module for a refresh token entity."""
import dataclasses
from dataclasses import dataclass
from datetime import datetime

from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.modules.identity.tokens.access_token import AccessTokenEntity
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier

RefreshTokenIdentifier = IntIdentifier


@dataclass(frozen=True, kw_only=True)
class RefreshTokenEntity:
    """A refresh token entity."""

    access_token: AccessTokenEntity
    id: RefreshTokenIdentifier = RefreshTokenIdentifier()
    identifier: TokenIdentifier = TokenIdentifier.generate()
    expiration: datetime = datetime.utcnow()
    revoked: bool = False
    traceable_time: TraceableTime = TraceableTime()

    @property
    def expired(self) -> bool:
        return self.expiration < datetime.utcnow()

    def revoke(self) -> "RefreshTokenEntity":
        """Revoke the refresh token."""
        return dataclasses.replace(
            self, revoked=True, access_token=self.access_token.revoke()
        )
