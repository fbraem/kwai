"""Module that implements a user recovery entity."""

from dataclasses import dataclass, field, replace
from typing import ClassVar, Self, Type

from kwai.core.domain.entity import DataclassEntity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.users.user import UserEntity


class UserRecoveryIdentifier(IntIdentifier):
    """Identifier for a user recovery entity."""


@dataclass(kw_only=True, eq=False, slots=True, frozen=True)
class UserRecoveryEntity(DataclassEntity):
    """A user recovery entity."""

    ID: ClassVar[Type] = UserRecoveryIdentifier

    user: UserEntity
    expiration: Timestamp = field(default_factory=Timestamp)
    uuid: UniqueId = field(default_factory=UniqueId.generate)
    remark: str = ""
    confirmation: Timestamp = field(default_factory=Timestamp)
    mailed_at: Timestamp = field(default_factory=Timestamp)

    def confirm(self) -> Self:
        """Confirm the user recovery."""
        return replace(
            self,
            confirmation=Timestamp.create_now(),
            traceable_time=self.traceable_time.mark_for_update(),
        )

    @property
    def confirmed(self) -> bool:
        """Return True when this user recovery was confirmed."""
        return not self.confirmation.empty

    @property
    def is_expired(self) -> bool:
        """Return True when the user recovery is expired."""
        return self.expiration.is_past

    @property
    def mailed(self) -> bool:
        """Return True if the email has already been sent."""
        return not self.mailed_at.empty

    def mail_sent(self):
        """Set the timestamp when mail has been sent."""
        return replace(
            self,
            mailed_at=Timestamp.create_now(),
            traceable_time=self.traceable_time.mark_for_update(),
        )
