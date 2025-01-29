"""Module that implements a refresh token query for a database."""

from typing import Self

from sql_smith.functions import on

from kwai.core.db.database_query import DatabaseQuery
from kwai.modules.identity.tokens.refresh_token_query import RefreshTokenQuery
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.tokens.token_tables import (
    AccessTokenRow,
    RefreshTokenRow,
)
from kwai.modules.identity.users.user_account import UserAccountEntity
from kwai.modules.identity.users.user_tables import UserAccountRow


class RefreshTokenDbQuery(RefreshTokenQuery, DatabaseQuery):
    """A refresh token query for a database."""

    def init(self):
        self._query.from_(RefreshTokenRow.__table_name__).join(
            AccessTokenRow.__table_name__,
            on(
                RefreshTokenRow.column("access_token_id"),
                AccessTokenRow.column("id"),
            ),
        ).join(
            UserAccountRow.__table_name__,
            on(AccessTokenRow.column("user_id"), UserAccountRow.column("id")),
        )

    @property
    def columns(self):
        return (
            RefreshTokenRow.get_aliases()
            + AccessTokenRow.get_aliases()
            + UserAccountRow.get_aliases()
        )

    def filter_by_id(self, id_: int) -> Self:
        self._query.and_where(RefreshTokenRow.field("id").eq(id_))
        return self

    def filter_by_token_identifier(self, identifier: TokenIdentifier) -> Self:
        self._query.and_where(RefreshTokenRow.field("identifier").eq(str(identifier)))
        return self

    def filter_by_user_account(self, user_account: UserAccountEntity) -> Self:
        self._query.and_where(UserAccountRow.field("id").eq(user_account.id.value))
        return self
