"""Module that defines an access token entity."""
from datetime import datetime
import dataclasses

from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.users import UserAccountEntity

AccessTokenIdentifier = IntIdentifier


@dataclasses.dataclass(kw_only=True, frozen=True)
class AccessTokenEntity:
    """An access token domain object."""

    user_account: UserAccountEntity
    id: AccessTokenIdentifier = IntIdentifier()
    identifier: TokenIdentifier = TokenIdentifier.generate()
    expiration: datetime = datetime.utcnow()
    revoked: bool = False
    traceable_time: TraceableTime = TraceableTime()

    @property
    def is_expired(self) -> bool:
        return self.expiration < datetime.utcnow()

    def revoke(self) -> "AccessTokenEntity":
        """Revoke the access token."""
        return dataclasses.replace(self, revoked=True)
