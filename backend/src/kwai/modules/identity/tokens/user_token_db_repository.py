"""Module that implements a user token repository for a database."""

from sql_smith.functions import express, field

from kwai.core.db.database import Database
from kwai.modules.identity.tokens.token_tables import AccessTokenRow, RefreshTokenRow
from kwai.modules.identity.tokens.user_token_repository import UserTokenRepository
from kwai.modules.identity.users.user_account import UserAccountEntity


class UserTokenDbRepository(UserTokenRepository):
    """Implements a user token repository for a database."""

    def __init__(self, database: Database):
        self._database = database

    async def revoke(self, user_account: UserAccountEntity):
        query_factory = Database.create_query_factory()

        update_access_token_query = query_factory.update(
            AccessTokenRow.__table_name__, {"revoked": 1}
        ).where(field(AccessTokenRow.column("user_id")).eq(user_account.id.value))
        await self._database.execute(update_access_token_query)

        select_access_tokens = (
            query_factory.select(AccessTokenRow.column("id"))
            .from_(AccessTokenRow.__table_name__)
            .where(AccessTokenRow.field("user_id").eq(user_account.id.value))
        )

        update_refresh_token_query = query_factory.update(
            RefreshTokenRow.__table_name__, {"revoked": 1}
        ).where(
            field(RefreshTokenRow.column("access_token_id")).in_(
                express("%s", select_access_tokens)
            )
        )
        await self._database.execute(update_refresh_token_query)
