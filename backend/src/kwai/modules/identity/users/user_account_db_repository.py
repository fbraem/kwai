"""Module that implements a user account repository for a database."""

from collections.abc import AsyncGenerator
from dataclasses import replace

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.modules.identity.users.user import UserIdentifier
from kwai.modules.identity.users.user_account import (
    UserAccountEntity,
    UserAccountIdentifier,
)
from kwai.modules.identity.users.user_account_repository import (
    UserAccountNotFoundException,
    UserAccountRepository,
)
from kwai.modules.identity.users.user_tables import (
    UserAccountRow,
)


class UserAccountDbRepository(UserAccountRepository):
    """User account repository for a database."""

    def __init__(self, database: Database):
        self._database = database

    async def get_all(
        self, limit: int | None = None, offset: int | None = None
    ) -> AsyncGenerator[UserAccountEntity]:
        query = (
            self._database.create_query_factory()
            .select()
            .from_(UserAccountRow.__table_name__)
            .columns(*UserAccountRow.get_aliases())
            .offset(offset)
            .limit(limit)
        )
        async for row in self._database.fetch(query):
            yield UserAccountRow.map(row).create_entity()

    async def get_user_by_email(self, email: EmailAddress) -> UserAccountEntity:
        query = (
            self._database.create_query_factory()
            .select()
            .from_(UserAccountRow.__table_name__)
            .columns(*UserAccountRow.get_aliases())
            .and_where(UserAccountRow.field("email").eq(str(email)))
        )
        row = await self._database.fetch_one(query)
        if row:
            return UserAccountRow.map(row).create_entity()

        raise UserAccountNotFoundException()

    async def exists_with_email(self, email: EmailAddress) -> bool:
        try:
            await self.get_user_by_email(email)
        except UserAccountNotFoundException:
            return False

        return True

    async def create(self, user_account: UserAccountEntity) -> UserAccountEntity:
        new_id = await self._database.insert(
            UserAccountRow.__table_name__, UserAccountRow.persist(user_account)
        )
        user = user_account.user.set_id(UserIdentifier(new_id))
        return replace(user_account, user=user).set_id(UserAccountIdentifier(new_id))

    async def update(self, user_account: UserAccountEntity):
        await self._database.update(
            user_account.id.value,
            UserAccountRow.__table_name__,
            UserAccountRow.persist(user_account),
        )

    async def delete(self, user_account):
        await self._database.delete(
            user_account.id.value, UserAccountRow.__table_name__
        )
