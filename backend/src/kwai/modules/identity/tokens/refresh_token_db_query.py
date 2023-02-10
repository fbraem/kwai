"""Module that implements a refresh token query for a database."""
from sql_smith.functions import on

from kwai.core.db.database_query import DatabaseQuery
from kwai.modules.identity.users.user_tables import UserAccountsTable
from .refresh_token_query import RefreshTokenQuery
from .token_identifier import TokenIdentifier
from .token_tables import (
    AccessTokensTable,
    RefreshTokensTable,
)


class RefreshTokenDbQuery(RefreshTokenQuery, DatabaseQuery):
    """A refresh token query for a database."""

    def init(self):
        self._query.from_(RefreshTokensTable.table_name).join(
            AccessTokensTable.table_name,
            on(
                RefreshTokensTable.column("access_token_id"),
                AccessTokensTable.column("id"),
            ),
        ).join(
            UserAccountsTable.table_name,
            on(AccessTokensTable.column("user_id"), UserAccountsTable.column("id")),
        )

    @property
    def columns(self):
        return (
            RefreshTokensTable.aliases()
            + AccessTokensTable.aliases()
            + UserAccountsTable.aliases()
        )

    def filter_by_id(self, id_: int) -> "RefreshTokenQuery":
        self._query.and_where(RefreshTokensTable.field("id").eq(id_))
        return self

    def filter_by_token_identifier(
        self, identifier: TokenIdentifier
    ) -> "RefreshTokenQuery":
        self._query.and_where(
            RefreshTokensTable.field("identifier").eq(str(identifier))
        )
        return self
