"""Module that defines an access token entity."""

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.users.user_account import UserAccountEntity

AccessTokenIdentifier = IntIdentifier


class AccessTokenEntity(Entity[AccessTokenIdentifier]):
    """An access token entity."""

    def __init__(
        self,
        *,
        id_: AccessTokenIdentifier | None = None,
        user_account: UserAccountEntity,
        identifier: TokenIdentifier | None = None,
        expiration: Timestamp | None = None,
        revoked: bool = False,
        traceable_time: TraceableTime | None = None,
    ):
        super().__init__(id_ or AccessTokenIdentifier())
        self._user_account = user_account
        self._identifier = identifier or TokenIdentifier.generate()
        self._expiration = expiration or Timestamp.create_now()
        self._revoked = revoked
        self._traceable_time = traceable_time or TraceableTime()

    @property
    def expiration(self) -> Timestamp:
        """Return the expiration timestamp of the access token."""
        return self._expiration

    @property
    def expired(self) -> bool:
        """Return true when the access token is expired."""
        return self._expiration.is_past

    @property
    def identifier(self) -> TokenIdentifier:
        """Return the identifier of the access token."""
        return self._identifier

    def revoke(self) -> None:
        """Revoke the access token."""
        self._revoked = True
        self._traceable_time = self._traceable_time.mark_for_update()

    @property
    def revoked(self) -> bool:
        """Return True when the access token is revoked."""
        return self._revoked

    @property
    def traceable_time(self) -> TraceableTime:
        """Return the creation/modification timestamps."""
        return self._traceable_time

    @property
    def user_account(self) -> UserAccountEntity:
        """Return the user of this access token."""
        return self._user_account
