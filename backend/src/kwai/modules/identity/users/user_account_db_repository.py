"""Module that implements a user account repository for a database."""
from kwai.core.db.database import Database
from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.modules.identity.users.user import UserIdentifier
from kwai.modules.identity.users.user_account import (
    UserAccountEntity,
    UserAccountIdentifier,
)
from kwai.modules.identity.users.user_account_repository import (
    UserAccountRepository,
    UserAccountNotFoundException,
)
from kwai.modules.identity.users.user_tables import (
    UserAccountsTable,
    UserAccountRow,
)


class UserAccountDbRepository(UserAccountRepository):
    """User account repository for a database."""

    def __init__(self, database: Database):
        self._database = database

    def get_user_by_email(self, email: EmailAddress) -> UserAccountEntity:
        query = (
            self._database.create_query_factory()
            .select()
            .from_(UserAccountsTable.table_name)
            .columns(*UserAccountsTable.aliases())
            .and_where(UserAccountsTable.field("email").eq(str(email)))
        )
        row = self._database.fetch_one(query)
        if row:
            return UserAccountsTable(row).create_entity()

        raise UserAccountNotFoundException()

    def exists_with_email(self, email: EmailAddress) -> bool:
        try:
            self.get_user_by_email(email)
        except UserAccountNotFoundException:
            return False

        return True

    def create(self, user_account: UserAccountEntity) -> UserAccountEntity:
        new_id = self._database.insert(
            UserAccountsTable.table_name, UserAccountRow.persist(user_account)
        )
        self._database.commit()
        return Entity.replace(
            user_account,
            id_=UserAccountIdentifier(new_id),
            user=Entity.replace(user_account.user, id_=UserIdentifier(new_id)),
        )

    def update(self, user_account: UserAccountEntity):
        self._database.update(
            user_account.id.value,
            UserAccountsTable.table_name,
            UserAccountRow.persist(user_account),
        )
        self._database.commit()

    def delete(self, user_account):
        self._database.delete(user_account.id.value, UserAccountsTable.table_name)
        self._database.commit()
