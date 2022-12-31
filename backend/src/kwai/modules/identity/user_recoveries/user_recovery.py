"""Module that implements a user recovery entity."""
from dataclasses import dataclass
from datetime import datetime

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects import UniqueId, TraceableTime, LocalTimestamp
from kwai.modules.identity.users import UserEntity


@dataclass
class UserRecovery:
    """A user recovery domain."""

    uuid: UniqueId
    expiration: LocalTimestamp
    user: UserEntity
    remark: str | None = None
    confirmation: datetime | None = None
    traceable_time: TraceableTime = TraceableTime()

    def confirm(self):
        """Confirms the user recovery."""
        self.confirmation = datetime.utcnow()


class UserRecoveryEntity(Entity[UserRecovery]):
    """An entity for a user recovery domain."""
