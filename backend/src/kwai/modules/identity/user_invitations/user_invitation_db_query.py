"""Module that implements a UserInvitationQuery for a database."""

from sql_smith.functions import on

from kwai.core.db.database_query import DatabaseQuery
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.user_invitations.user_invitation import (
    UserInvitationIdentifier,
)
from kwai.modules.identity.user_invitations.user_invitation_query import (
    UserInvitationQuery,
)
from kwai.modules.identity.user_invitations.user_invitation_tables import (
    UserInvitationRow,
)
from kwai.modules.identity.users.user_tables import UserRow


class UserInvitationDbQuery(UserInvitationQuery, DatabaseQuery):
    """A database query for a user invitation."""

    def init(self):
        return self._query.from_(UserInvitationRow.__table_name__).join(
            UserRow.__table_name__,
            on(UserInvitationRow.column("user_id"), UserRow.column("id")),
        )

    @property
    def columns(self):
        return UserInvitationRow.get_aliases() + UserRow.get_aliases()

    @property
    def count_column(self) -> str:
        return UserInvitationRow.column("id")

    def filter_by_id(self, id_: UserInvitationIdentifier) -> "UserInvitationQuery":
        self._query.and_where(UserInvitationRow.field("id").eq(id_.value))
        return self

    def filter_by_uuid(self, uuid: UniqueId) -> "UserInvitationQuery":
        self._query.and_where(UserInvitationRow.field("uuid").eq(str(uuid)))
        return self

    def filter_by_email(self, email: EmailAddress) -> "UserInvitationQuery":
        self._query.and_where(UserInvitationRow.field("email").eq(str(email)))
        return self

    def filter_active(self) -> "UserInvitationQuery":
        self._query.and_where(UserInvitationRow.field("revoked").not_eq(1))
        return self

    def filter_not_expired(self, timestamp: Timestamp) -> "UserInvitationQuery":
        self._query.and_where(UserInvitationRow.field("expired_at").gt(str(timestamp)))
        return self

    def filter_not_confirmed(self) -> "UserInvitationQuery":
        self._query.and_where(UserInvitationRow.field("confirmed_at").is_null())
        return self
