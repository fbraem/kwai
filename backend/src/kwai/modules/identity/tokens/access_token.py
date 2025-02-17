"""Module that defines an access token entity."""

from dataclasses import dataclass, field, replace
from typing import ClassVar, Self, Type

from kwai.core.domain.entity import DataclassEntity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.users.user_account import UserAccountEntity


class AccessTokenIdentifier(IntIdentifier):
    """Identifier for an access token."""


@dataclass(kw_only=True, eq=False, slots=True, frozen=True)
class AccessTokenEntity(DataclassEntity):
    """An access token entity.

    Attributes:
        user_account: The user account associated with this token.
        identifier: The actual token.
        expiration: The expiration timestamp of the token.
        revoked: Whether the token has been revoked.
    """

    ID: ClassVar[Type] = AccessTokenIdentifier

    user_account: UserAccountEntity
    identifier: TokenIdentifier = field(default_factory=TokenIdentifier.generate)
    expiration: Timestamp = field(default_factory=Timestamp.create_now)
    revoked: bool = field(default=False)

    @property
    def expired(self) -> bool:
        """Return true when the access token is expired."""
        return self.expiration.is_past

    def revoke(self) -> Self:
        """Revoke the access token.

        Returns:
            A revoked access token.
        """
        return replace(
            self, revoked=True, traceable_time=self.traceable_time.mark_for_update()
        )

    def renew(self, expiry_minutes: int) -> Self:
        """Renew the access token."""
        return replace(
            self,
            identifier=TokenIdentifier.generate(),
            expiration=Timestamp.create_with_delta(minutes=expiry_minutes),
            traceable_time=self.traceable_time.mark_for_update(),
        )
