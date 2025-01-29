"""Module that implements an access token query for a database."""

from typing import Self

from sql_smith.functions import on

from kwai.core.db.database_query import DatabaseQuery
from kwai.modules.identity.users.user_account import UserAccountEntity
from kwai.modules.identity.users.user_tables import UserAccountRow

from .access_token import AccessTokenIdentifier
from .access_token_query import AccessTokenQuery
from .token_identifier import TokenIdentifier
from .token_tables import AccessTokenRow


class AccessTokenDbQuery(AccessTokenQuery, DatabaseQuery):
    """An access token query for a database."""

    def init(self):
        self._query.from_(AccessTokenRow.__table_name__).join(
            UserAccountRow.__table_name__,
            on(AccessTokenRow.column("user_id"), UserAccountRow.column("id")),
        )

    @property
    def columns(self):
        return AccessTokenRow.get_aliases() + UserAccountRow.get_aliases()

    def filter_by_id(self, id_: AccessTokenIdentifier) -> "AccessTokenQuery":
        self._query.and_where(AccessTokenRow.field("id").eq(id_.value))
        return self

    def filter_by_token_identifier(
        self, identifier: TokenIdentifier
    ) -> "AccessTokenQuery":
        self._query.and_where(AccessTokenRow.field("identifier").eq(str(identifier)))
        return self

    def filter_by_user_account(self, user_account: UserAccountEntity) -> Self:
        self._query.and_where(AccessTokenRow.field("user_id").eq(user_account.id.value))
        return self
