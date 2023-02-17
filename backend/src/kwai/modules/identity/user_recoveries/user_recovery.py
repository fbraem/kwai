"""Module that implements a user recovery entity."""
from dataclasses import dataclass, field

from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.users.user import UserEntity

UserRecoveryIdentifier = IntIdentifier


@dataclass(kw_only=True)
class UserRecoveryEntity:
    """A user recovery domain."""

    # pylint: disable=too-many-instance-attributes
    user: UserEntity
    expiration: LocalTimestamp = field(default_factory=LocalTimestamp)
    id: UserRecoveryIdentifier = field(default_factory=UserRecoveryIdentifier)
    uuid: UniqueId = field(default_factory=UniqueId.generate)
    remark: str | None = None
    confirmation: LocalTimestamp() = field(default_factory=LocalTimestamp)
    mailed_at: LocalTimestamp() = field(default_factory=LocalTimestamp)
    traceable_time: TraceableTime = field(default_factory=TraceableTime)

    def confirm(self):
        """Confirm the user recovery."""
        self.confirmation = LocalTimestamp.create_now()
        self.traceable_time = self.traceable_time.mark_for_update()

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
        """Return True when the mail was already send."""
        return not self.mailed_at.empty

    def mail_send(self):
        """Set the timestamp when mail has been sent."""
        self.mailed_at = LocalTimestamp.create_now()
        self.traceable_time = self.traceable_time.mark_for_update()
