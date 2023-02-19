"""Module for a refresh token entity."""
from datetime import datetime

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.modules.identity.tokens.access_token import AccessTokenEntity
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier

RefreshTokenIdentifier = IntIdentifier


class RefreshTokenEntity(Entity[RefreshTokenIdentifier]):
    """A refresh token entity."""

    def __init__(
        self,
        *,
        id_: RefreshTokenIdentifier | None = None,
        access_token: AccessTokenEntity,
        identifier: TokenIdentifier | None = None,
        expiration: datetime | None,
        revoked: bool = False,
        traceable_time: TraceableTime | None = None,
    ):
        super().__init__(id_ or RefreshTokenIdentifier())
        self._access_token = access_token
        self._identifier = identifier or TokenIdentifier.generate()
        self._expiration = expiration or datetime.utcnow()
        self._revoked = revoked
        self._traceable_time = traceable_time or TraceableTime()

    @property
    def access_token(self) -> AccessTokenEntity:
        """Return the associated access token."""
        return self._access_token

    @property
    def expiration(self) -> datetime:
        """Return the expiration timestamp of the refresh token."""
        return self._expiration

    @property
    def expired(self) -> bool:
        """Return True when the token is expired."""
        return self._expiration < datetime.utcnow()

    @property
    def identifier(self) -> TokenIdentifier:
        """Return the identifier of the refresh token."""
        return self._identifier

    def revoke(self) -> None:
        """Revoke the refresh token."""
        self._revoked = True
        self._access_token.revoke()
        self._traceable_time = self._traceable_time.mark_for_update()

    @property
    def revoked(self) -> bool:
        """Return True when the refresh token is revoked."""
        return self._revoked

    @property
    def traceable_time(self) -> TraceableTime:
        """Return the creation/modification timestamps."""
        return self._traceable_time
