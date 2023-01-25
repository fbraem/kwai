"""Module that defines an access token entity."""
from datetime import datetime
import dataclasses

from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.users.user_account import UserAccountEntity

AccessTokenIdentifier = IntIdentifier


@dataclasses.dataclass(kw_only=True)
class AccessTokenEntity:
    """An access token entity."""

    user_account: UserAccountEntity
    id: AccessTokenIdentifier = AccessTokenIdentifier()
    identifier: TokenIdentifier = TokenIdentifier.generate()
    expiration: datetime = datetime.utcnow()
    revoked: bool = False
    traceable_time: TraceableTime = TraceableTime()

    @property
    def expired(self) -> bool:
        return self.expiration < datetime.utcnow()

    def revoke(self) -> None:
        """Revoke the access token."""
        self.revoked = True
