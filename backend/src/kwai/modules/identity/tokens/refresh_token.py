"""Module for a refresh token entity."""

from dataclasses import dataclass, field, replace
from typing import ClassVar, Self, Type

from kwai.core.domain.entity import DataclassEntity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.modules.identity.tokens.access_token import AccessTokenEntity
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier


class RefreshTokenIdentifier(IntIdentifier):
    """Identifier for a refresh token."""


@dataclass(kw_only=True, eq=False, slots=True, frozen=True)
class RefreshTokenEntity(DataclassEntity):
    """A refresh token entity.

    Attributes:
        access_token: The access token associated with this refresh token.
        identifier: The actual token.
        expiration: The expiration timestamp of the token.
        revoked: Whether the token has been revoked.
    """

    ID: ClassVar[Type] = RefreshTokenIdentifier

    access_token: AccessTokenEntity
    identifier: TokenIdentifier = field(default_factory=TokenIdentifier.generate)
    expiration: Timestamp = field(default_factory=Timestamp.create_now)
    revoked: bool = field(default=False)

    @property
    def expired(self) -> bool:
        """Return True when the token is expired."""
        return self.expiration.is_past

    def revoke(self) -> Self:
        """Revoke the refresh token.

        Returns:
            A revoked refresh token.
        """
        return replace(
            self, revoked=True, traceable_time=self.traceable_time.mark_for_update()
        )
