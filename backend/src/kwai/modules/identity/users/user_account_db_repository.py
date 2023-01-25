"""Module that implements a user account repository for a database."""
import dataclasses
from typing import Any

from kwai.core.db import Database
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.modules.identity.users.user_account import UserAccountEntity, UserAccount
from kwai.modules.identity.users.user_account_repository import (
    UserAccountRepository,
    UserAccountNotFoundException,
)
from kwai.modules.identity.users.user_tables import (
    UserAccountsTable,
    UserAccountMapper,
)


def map_user_account(row: dict[str, Any]) -> UserAccountEntity:
    """Create a user account entity from a row."""
    return UserAccountMapper(
        user_accounts_table=UserAccountsTable.map_row(row)
    ).create_entity()


class UserAccountDbRepository(UserAccountRepository):
    def __init__(self, database: Database):
        self._database = database

    def get_user_by_email(self, email: EmailAddress) -> UserAccountEntity:
        query = (
            self._database.create_query_factory()
            .select()
            .from_(UserAccountsTable.__table_name__)
            .columns(*UserAccountsTable.aliases())
            .and_where(UserAccountsTable.field("email").eq(str(email)))
        )
        row = self._database.fetch_one(query)
        if row:
            return map_user_account(row)

        raise UserAccountNotFoundException()

    def create(self, user_account: UserAccount) -> UserAccountEntity:
        record = dataclasses.asdict(UserAccountsTable.persist(user_account))
        del record["id"]
        query = (
            self._database.create_query_factory()
            .insert(UserAccountsTable.__table_name__)
            .columns(*record.keys())
            .values(*record.values())
        )
        last_insert_id = self._database.execute(query)
        self._database.commit()
        return UserAccountEntity(id=last_insert_id, domain=user_account)

    def update(self, user_account_entity: UserAccountEntity):
        record = dataclasses.asdict(
            UserAccountsTable.persist(user_account_entity.domain)
        )
        del record["id"]
        query = (
            self._database.create_query_factory()
            .update(UserAccountsTable.__table_name__)
            .set(record)
            .where(UserAccountsTable.field("id").eq(user_account_entity.id))
        )
        self._database.execute(query)
        self._database.commit()

    def delete(self, user_account_entity):
        query = (
            self._database.create_query_factory()
            .delete(UserAccountsTable.__table_name__)
            .where(UserAccountsTable.field("id").eq(user_account_entity.id))
        )
        self._database.execute(query)
        self._database.commit()
