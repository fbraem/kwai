"""Module that defines the table for a user recovery."""
from dataclasses import dataclass
from datetime import datetime

from kwai.core.db.table import table
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.user_recoveries.user_recovery import (
    UserRecoveryIdentifier,
    UserRecoveryEntity,
)
from kwai.modules.identity.users.user_tables import UserMapper


@table(name="user_recoveries")
@dataclass
class UserRecoveriesTable:
    """Table for a user recovery."""

    # pylint: disable=too-many-instance-attributes

    id: int | None
    user_id: int
    uuid: str
    expired_at: datetime
    expired_at_timezone: str
    confirmed_at: datetime | None
    mailed_at: datetime | None
    remark: str | None
    created_at: datetime
    updated_at: datetime | None

    @classmethod
    def persist(cls, user_recovery: UserRecoveryEntity) -> "UserRecoveriesTable":
        """Map a user recovery entity to a table record."""
        return UserRecoveriesTable(
            id=user_recovery.id.value,
            user_id=user_recovery.user.id.value,
            uuid=str(user_recovery.uuid),
            expired_at=user_recovery.expiration.timestamp,
            expired_at_timezone=user_recovery.expiration.timezone,
            confirmed_at=user_recovery.confirmation.timestamp,
            mailed_at=user_recovery.mailed_at.timestamp,
            remark=user_recovery.remark,
            created_at=user_recovery.traceable_time.created_at,
            updated_at=user_recovery.traceable_time.updated_at,
        )


@dataclass(kw_only=True, frozen=True)
class UserRecoveryMapper:
    """Mapper for creating a user recovery entity from a table record."""

    user_recoveries_table: UserRecoveriesTable
    user_mapper: UserMapper

    def create_entity(self) -> UserRecoveryEntity:
        """Create the entity."""
        return UserRecoveryEntity(
            id=UserRecoveryIdentifier(self.user_recoveries_table.id),
            uuid=UniqueId.create_from_string(self.user_recoveries_table.uuid),
            user=self.user_mapper.create_entity(),
            expiration=LocalTimestamp(
                self.user_recoveries_table.expired_at,
                self.user_recoveries_table.expired_at_timezone,
            ),
            remark=self.user_recoveries_table.remark,
            confirmation=LocalTimestamp(self.user_recoveries_table.confirmed_at),
            mailed_at=LocalTimestamp(self.user_recoveries_table.mailed_at),
            traceable_time=TraceableTime(
                created_at=self.user_recoveries_table.created_at,
                updated_at=self.user_recoveries_table.updated_at,
            ),
        )
