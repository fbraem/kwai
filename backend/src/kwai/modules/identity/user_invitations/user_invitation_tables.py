"""Module that defines all dataclasses for the tables containing invitations."""
from dataclasses import dataclass
from datetime import datetime

from kwai.core.db.table import Table
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.user_invitations.user_invitation import (
    UserInvitationEntity,
    UserInvitationIdentifier,
)
from kwai.modules.identity.users.user import UserEntity


# pylint: disable=too-many-instance-attributes


@dataclass(kw_only=True, frozen=True, slots=True)
class UserInvitationRow:
    """Represent a table row in the invitations table.

    Attributes:
        id(int): the id of the invitation
        email(str): the email that received this invitation
        first_name(str): the firstname of the invited
        last_name(str): the lastname of the invited
        uuid(str): a unique uuid for the invitation
        expired_at(datetime): the timestamp when the invitation expires
        expired_at_timezone(str): the timezone of the expiration date
        remark(str|None): a remark about the invitation
        user_id(int): the user that created the invitation
        confirmed_at(datetime|None): the timestamp when the invitation was used
        revoked(bool): is the invitation revoked?
        created_at(datetime): the timestamp of creation
        updated_at(datetime|None): the timestamp of the last modification
    """

    id: int
    email: str
    first_name: str
    last_name: str
    uuid: str
    expired_at: datetime
    expired_at_timezone: str
    remark: str | None
    user_id: int
    confirmed_at: datetime | None
    revoked: int
    created_at: datetime
    updated_at: datetime | None

    def create_entity(self, user: UserEntity) -> UserInvitationEntity:
        return UserInvitationEntity(
            id_=UserInvitationIdentifier(self.id),
            email=EmailAddress(self.email),
            name=Name(last_name=self.last_name, first_name=self.first_name),
            uuid=UniqueId.create_from_string(self.uuid),
            expired_at=LocalTimestamp(self.expired_at),
            user=user,
            remark=self.remark or "",
            confirmed_at=LocalTimestamp(self.confirmed_at),
            revoked=True if self.revoked == 1 else False,
            traceable_time=TraceableTime(
                created_at=self.created_at, updated_at=self.updated_at
            ),
        )

    @classmethod
    def persist(cls, invitation: UserInvitationEntity) -> "UserInvitationRow":
        return UserInvitationRow(
            id=invitation.id.value,
            email=str(invitation.email),
            first_name=invitation.name.first_name,
            last_name=invitation.name.last_name,
            uuid=str(invitation.uuid),
            expired_at=invitation.expired_at.timestamp,
            expired_at_timezone=invitation.expired_at.timezone,
            remark=invitation.remark,
            user_id=invitation.user.id.value,
            confirmed_at=invitation.confirmed_at.timestamp,
            revoked=1 if invitation.revoked else 0,
            created_at=invitation.traceable_time.created_at,
            updated_at=invitation.traceable_time.updated_at,
        )


UserInvitationsTable = Table("user_invitations", UserInvitationRow)
