"""Module that implements the UserQuery interface for a database."""
from kwai.core.db.database_query import DatabaseQuery
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.users.user_query import UserQuery
from kwai.modules.identity.users.user_tables import UsersTable


class UserDbQuery(UserQuery, DatabaseQuery):
    """A user query for a database."""

    def init(self):
        self._query.from_(UsersTable.__table_name__)  # pylint: disable=no-member

    @property
    def columns(self):
        return UsersTable.aliases()  # pylint: disable=no-member

    def filter_by_id(self, id_: int) -> UserQuery:
        """Add a filter for a user with the given id."""
        self._query.and_where(
            UsersTable.field("id").eq(id_)  # pylint: disable=no-member
        )
        return self

    def filter_by_uuid(self, uuid: UniqueId) -> UserQuery:
        """Add a filter for a user with the given unique id."""
        self._query.and_where(
            UsersTable.field("uuid").eq(str(uuid))  # pylint: disable=no-member
        )
        return self

    def filter_by_email(self, email: EmailAddress) -> UserQuery:
        """Add a filter for a user with the given email address."""
        self._query.and_where(
            UsersTable.field("email").eq(str(email))  # pylint: disable=no-member
        )
        return self
