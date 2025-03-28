"""Module that implements the UserQuery interface for a database."""

from kwai.core.db.database_query import DatabaseQuery
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.users.user import UserIdentifier
from kwai.modules.identity.users.user_query import UserQuery
from kwai.modules.identity.users.user_tables import UserRow


class UserDbQuery(UserQuery, DatabaseQuery):
    """A user query for a database."""

    def init(self):
        self._query.from_(UserRow.__table_name__)

    @property
    def columns(self):
        return UserRow.get_aliases()

    def filter_by_id(self, id_: UserIdentifier) -> UserQuery:
        """Add a filter for a user with the given id."""
        self._query.and_where(UserRow.field("id").eq(id_.value))
        return self

    def filter_by_uuid(self, uuid: UniqueId) -> UserQuery:
        """Add a filter for a user with the given unique id."""
        self._query.and_where(UserRow.field("uuid").eq(str(uuid)))
        return self

    def filter_by_email(self, email: EmailAddress) -> UserQuery:
        """Add a filter for a user with the given email address."""
        self._query.and_where(UserRow.field("email").eq(str(email)))
        return self
