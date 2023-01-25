"""Module that implements a user recovery entity."""
from dataclasses import dataclass
from datetime import datetime

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.users.user import UserEntity


@dataclass
class UserRecovery:
    """A user recovery domain."""

    uuid: UniqueId
    expiration: LocalTimestamp
    user: UserEntity
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


class UserRecoveryEntity(Entity[UserRecovery]):
    """An entity for a user recovery domain."""
