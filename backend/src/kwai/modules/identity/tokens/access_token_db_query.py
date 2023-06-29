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
        """Initialize the query."""
        self._query.from_(AccessTokensTable.table_name).join(
            UserAccountsTable.table_name,
            on(AccessTokensTable.column("user_id"), UserAccountsTable.column("id")),
        )

    @property
    def columns(self):
        """Return the columns for the query."""
        return AccessTokensTable.aliases() + UserAccountsTable.aliases()

    def filter_by_id(self, id_: int) -> "AccessTokenQuery":
        """Add a filter for id."""
        self._query.and_where(AccessTokensTable.field("id").eq(id_))
        return self

    def filter_by_token_identifier(
        self, identifier: TokenIdentifier
    ) -> "AccessTokenQuery":
        """Add a filter for a token identifier."""
        self._query.and_where(AccessTokensTable.field("identifier").eq(str(identifier)))
        return self
