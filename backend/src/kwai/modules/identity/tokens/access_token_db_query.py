"""Module that implements an access token query for a database."""
from sql_smith.functions import on

from kwai.core.db.database_query import DatabaseQuery
from kwai.modules.identity.users.user_tables import UserAccountsTable
from .access_token_query import AccessTokenQuery
from .token_identifier import TokenIdentifier
from .token_tables import AccessTokensTable


class AccessTokenDbQuery(AccessTokenQuery, DatabaseQuery):
    """An access token query for a database."""

    def init(self):
        self._query.from_(AccessTokensTable.__table_name__).join(
            UserAccountsTable.__table_name__,
            on(AccessTokensTable.column("user_id"), UserAccountsTable.column("id")),
        )

    @property
    def columns(self):
        return AccessTokensTable.aliases() + UserAccountsTable.aliases()

    def filter_by_id(self, id_: int) -> "AccessTokenQuery":
        self._query.and_where(AccessTokensTable.field("id").eq(id_))
        return self

    def filter_by_token_identifier(
        self, identifier: TokenIdentifier
    ) -> "AccessTokenQuery":
        self._query.and_where(AccessTokensTable.field("identifier").eq(str(identifier)))
        return self
