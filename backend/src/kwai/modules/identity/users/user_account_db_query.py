"""Module that implements the UserAccountQuery interface for a database."""

from typing import Self

from kwai.core.db.database_query import DatabaseQuery
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.users.user_account import UserAccountIdentifier
from kwai.modules.identity.users.user_account_query import UserAccountQuery
from kwai.modules.identity.users.user_tables import UserAccountRow


class UserAccountDbQuery(UserAccountQuery, DatabaseQuery):
    """A user account query for a database."""

    def init(self):
        self._query.from_(UserAccountRow.__table_name__)

    @property
    def columns(self):
        return UserAccountRow.get_aliases()

    def filter_by_id(self, id_: UserAccountIdentifier) -> Self:
        self._query.and_where(UserAccountRow.field("id").eq(id_.value))
        return self

    def filter_by_email(self, email: EmailAddress) -> Self:
        self._query.and_where(UserAccountRow.field("email").eq(str(email)))
        return self

    def filter_by_uuid(self, uuid: UniqueId) -> Self:
        self._query.and_where(UserAccountRow.field("uuid").eq(str(uuid)))
        return self
