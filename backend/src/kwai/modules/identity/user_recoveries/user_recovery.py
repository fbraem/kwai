"""Module that implements a user recovery entity."""
from dataclasses import dataclass
from datetime import datetime

from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.users.user import UserEntity

UserRecoveryIdentifier = IntIdentifier


@dataclass
class UserRecoveryEntity:
    """A user recovery domain."""

    expiration: LocalTimestamp
    user: UserEntity
    id: UserRecoveryIdentifier = UserRecoveryIdentifier(0)
    uuid: UniqueId = UniqueId.generate()
    remark: str | None = None
    confirmation: datetime | None = None
    mailed: datetime | None = None
    traceable_time: TraceableTime = TraceableTime()

    def confirm(self):
        """Confirms the user recovery."""
        self.confirmation = datetime.utcnow()

    @property
    def confirmed(self) -> bool:
        """Returns True when this user recovery was confirmed."""
        return self.confirmation is not None

    def mail_send(self):
        """Sets the timestamp when mail has been sent."""
        self.mailed = datetime.utcnow()
