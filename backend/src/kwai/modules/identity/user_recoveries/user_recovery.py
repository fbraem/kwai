"""Module that implements a user recovery entity."""
from dataclasses import dataclass

from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.users.user import UserEntity

UserRecoveryIdentifier = IntIdentifier


@dataclass(kw_only=True)
class UserRecoveryEntity:
    """A user recovery domain."""

    user: UserEntity
    expiration: LocalTimestamp = LocalTimestamp()
    id: UserRecoveryIdentifier = UserRecoveryIdentifier(0)
    uuid: UniqueId = UniqueId.generate()
    remark: str | None = None
    confirmation: LocalTimestamp() = LocalTimestamp()
    mailed_at: LocalTimestamp() = LocalTimestamp()
    traceable_time: TraceableTime = TraceableTime()

    def confirm(self):
        """Confirms the user recovery."""
        self.confirmation = LocalTimestamp.create_now()
        self.traceable_time = self.traceable_time.mark_for_update()

    @property
    def confirmed(self) -> bool:
        """Returns True when this user recovery was confirmed."""
        return not self.confirmation.empty

    @property
    def is_expired(self) -> bool:
        """Return True when the user recovery is expired."""
        return self.expiration.is_past

    @property
    def mailed(self) -> bool:
        """Returns True when the mail was already send."""
        return not self.mailed_at.empty

    def mail_send(self):
        """Sets the timestamp when mail has been sent."""
        self.mailed_at = LocalTimestamp.create_now()
        self.traceable_time = self.traceable_time.mark_for_update()
