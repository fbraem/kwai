"""Module that defines the table for a user recovery."""

from dataclasses import dataclass
from datetime import datetime

from kwai.core.db.table import Table
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.user_recoveries.user_recovery import (
    UserRecoveryEntity,
    UserRecoveryIdentifier,
)
from kwai.modules.identity.users.user import UserEntity


@dataclass
class UserRecoveryRow:
    """Represent a row in the user recovery table."""

    id: int | None
    user_id: int
    uuid: str
    expired_at: datetime
    confirmed_at: datetime | None
    mailed_at: datetime | None
    remark: str | None
    created_at: datetime
    updated_at: datetime | None

    def create_entity(self, user: UserEntity) -> UserRecoveryEntity:
        """Create a user recovery entity from the table row."""
        return UserRecoveryEntity(
            id_=UserRecoveryIdentifier(self.id),
            uuid=UniqueId.create_from_string(self.uuid),
            user=user,
            expiration=Timestamp.create_utc(self.expired_at),
            remark=self.remark,
            confirmation=Timestamp.create_utc(self.confirmed_at),
            mailed_at=Timestamp.create_utc(self.mailed_at),
            traceable_time=TraceableTime(
                created_at=Timestamp.create_utc(timestamp=self.created_at),
                updated_at=Timestamp.create_utc(timestamp=self.updated_at),
            ),
        )

    @classmethod
    def persist(cls, user_recovery: UserRecoveryEntity) -> "UserRecoveryRow":
        """Map a user recovery entity to a table record."""
        return UserRecoveryRow(
            id=user_recovery.id.value,
            user_id=user_recovery.user.id.value,
            uuid=str(user_recovery.uuid),
            expired_at=user_recovery.expiration.timestamp,
            confirmed_at=user_recovery.confirmed_at.timestamp,
            mailed_at=user_recovery.mailed_at.timestamp,
            remark=user_recovery.remark,
            created_at=user_recovery.traceable_time.created_at.timestamp,
            updated_at=user_recovery.traceable_time.updated_at.timestamp,
        )


UserRecoveriesTable = Table("user_recoveries", UserRecoveryRow)
