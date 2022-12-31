"""Module that implements a user recovery repository interface for a database."""
from typing import Any

from sql_smith.functions import on

from kwai.core.db import Database
from kwai.core.domain.value_objects import UniqueId
from kwai.modules.identity.user_recoveries import (
    UserRecoveryEntity,
    UserRecovery,
    UserRecoveryRepository,
    UserRecoveryNotFoundException,
)
from kwai.modules.identity.user_recoveries.user_recovery_tables import (
    UserRecoveriesTable,
    UserRecoveryMapper,
)
from kwai.modules.identity.users.user_tables import UserMapper, UsersTable


def map_user_recovery(row: dict[str, Any]) -> UserRecoveryEntity:
    return UserRecoveryMapper(
        user_recoveries_table=UserRecoveriesTable.map_row(row),
        user_mapper=UserMapper(users_table=UsersTable.map_row(row)),
    ).create_entity()


class UserRecoveryDbRepository(UserRecoveryRepository):
    """A user recovery repository for a database."""

    def __init__(self, database: Database):
        self._database = database

    def create(self, user_recovery: UserRecovery) -> UserRecoveryEntity:
        id_ = self._database.insert(UserRecoveriesTable.persist(user_recovery))
        return UserRecoveryEntity(id=id_, domain=user_recovery)

    def update(self, user_recovery: UserRecoveryEntity):
        self._database.update(
            user_recovery.id, UserRecoveriesTable.persist(user_recovery.domain)
        )

    def get_by_uuid(self, uuid: UniqueId) -> UserRecoveryEntity:
        query = (
            self._database.create_query_factory()
            .select()
            .columns(*(UserRecoveriesTable.aliases() + UsersTable.aliases()))
            .from_(UserRecoveriesTable.__table_name__)
            .join(
                UsersTable.__table_name__,
                on(UserRecoveriesTable.column("user_id"), UsersTable.column("id")),
            )
            .and_where(UserRecoveriesTable.field("uuid").eq(str(uuid)))
        )
        row = self._database.fetch_one(query)
        if row:
            return map_user_recovery(row)

        raise UserRecoveryNotFoundException()

    def delete(self, user_recovery: UserRecoveryEntity):
        self._database.delete(user_recovery.id, UserRecoveriesTable.__table_name__)
        self._database.commit()
