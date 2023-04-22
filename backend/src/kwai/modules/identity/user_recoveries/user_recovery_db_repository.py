"""Module that implements a user recovery repository interface for a database."""
from typing import Any

from sql_smith.functions import on

from kwai.core.db.database import Database
from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.user_recoveries.user_recovery import (
    UserRecoveryIdentifier,
    UserRecoveryEntity,
)
from kwai.modules.identity.user_recoveries.user_recovery_repository import (
    UserRecoveryRepository,
    UserRecoveryNotFoundException,
)
from kwai.modules.identity.user_recoveries.user_recovery_tables import (
    UserRecoveriesTable,
    UserRecoveryRow,
)
from kwai.modules.identity.users.user_tables import UsersTable


def _create_entity(row: dict[str, Any]) -> UserRecoveryEntity:
    """Map the user recovery record to an entity."""
    return UserRecoveriesTable(row).create_entity(UsersTable(row).create_entity())


class UserRecoveryDbRepository(UserRecoveryRepository):
    """A user recovery repository for a database."""

    def __init__(self, database: Database):
        self._database = database

    async def create(self, user_recovery: UserRecoveryEntity) -> UserRecoveryEntity:
        new_id = await self._database.insert(
            UserRecoveriesTable.table_name, UserRecoveryRow.persist(user_recovery)
        )
        await self._database.commit()
        return Entity.replace(user_recovery, id_=UserRecoveryIdentifier(new_id))

    async def update(self, user_recovery: UserRecoveryEntity):
        await self._database.update(
            user_recovery.id.value,
            UserRecoveriesTable.table_name,
            UserRecoveryRow.persist(user_recovery),
        )
        await self._database.commit()

    async def get_by_uuid(self, uuid: UniqueId) -> UserRecoveryEntity:
        query = (
            self._database.create_query_factory()
            .select()
            .columns(*(UserRecoveriesTable.aliases() + UsersTable.aliases()))
            .from_(UserRecoveriesTable.table_name)
            .join(
                UsersTable.table_name,
                on(UserRecoveriesTable.column("user_id"), UsersTable.column("id")),
            )
            .and_where(UserRecoveriesTable.field("uuid").eq(str(uuid)))
        )
        if row := await self._database.fetch_one(query):
            return _create_entity(row)

        raise UserRecoveryNotFoundException()

    async def delete(self, user_recovery: UserRecoveryEntity):
        await self._database.delete(
            user_recovery.id.value, UserRecoveriesTable.table_name
        )
        await self._database.commit()
