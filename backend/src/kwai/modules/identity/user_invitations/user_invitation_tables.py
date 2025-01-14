"""Module that defines all dataclasses for the tables containing invitations."""

from dataclasses import dataclass
from datetime import datetime
from typing import Self

from kwai.core.db.table_row import TableRow
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.user_invitations.user_invitation import (
    UserInvitationEntity,
    UserInvitationIdentifier,
)
from kwai.modules.identity.users.user import UserEntity


@dataclass(kw_only=True, frozen=True, slots=True)
class UserInvitationRow(TableRow):
    """Represent a table row in the invitations table.

    Attributes:
        id(int): the id of the invitation
        email(str): the email that received this invitation
        first_name(str): the firstname of the invited
        last_name(str): the lastname of the invited
        uuid(str): a unique uuid for the invitation
        expired_at(datetime): the timestamp when the invitation expires
        remark(str|None): a remark about the invitation
        user_id(int): the user that created the invitation
        confirmed_at(datetime|None): the timestamp when the invitation was used
        revoked(bool): is the invitation revoked?
        created_at(datetime): the timestamp of creation
        updated_at(datetime|None): the timestamp of the last modification
        mailed_at(datetime|None): the timestamp of sending the email
    """

    __table_name__ = "user_invitations"

    id: int
    email: str
    first_name: str
    last_name: str
    uuid: str
    expired_at: datetime
    remark: str | None
    user_id: int
    confirmed_at: datetime | None
    revoked: int
    created_at: datetime
    updated_at: datetime | None
    mailed_at: datetime | None

    def create_entity(self, user: UserEntity) -> UserInvitationEntity:
        """Create a user invitation entity from the table row.

        Args:
            user: The associated user entity

        Returns:
            A user invitation entity.
        """
        return UserInvitationEntity(
            id=UserInvitationIdentifier(self.id),
            email=EmailAddress(self.email),
            name=Name(last_name=self.last_name, first_name=self.first_name),
            uuid=UniqueId.create_from_string(self.uuid),
            expired_at=Timestamp.create_utc(self.expired_at),
            user=user,
            remark=self.remark or "",
            mailed_at=Timestamp.create_utc(self.mailed_at),
            confirmed_at=Timestamp.create_utc(self.confirmed_at),
            revoked=self.revoked == 1,
            traceable_time=TraceableTime(
                created_at=Timestamp.create_utc(self.created_at),
                updated_at=Timestamp.create_utc(self.updated_at),
            ),
        )

    @classmethod
    def persist(cls, invitation: UserInvitationEntity) -> Self:
        """Persist a user invitation entity into a table row.

        Args:
            invitation: The user invitation entity to persist.

        Returns:
            A dataclass containing the table row data.
        """
        return UserInvitationRow(
            id=invitation.id.value,
            email=str(invitation.email),
            first_name=invitation.name.first_name,
            last_name=invitation.name.last_name,
            uuid=str(invitation.uuid),
            expired_at=invitation.expired_at.timestamp,
            mailed_at=invitation.mailed_at.timestamp,
            remark=invitation.remark,
            user_id=invitation.user.id.value,
            confirmed_at=invitation.confirmed_at.timestamp,
            revoked=1 if invitation.revoked else 0,
            created_at=invitation.traceable_time.created_at.timestamp,
            updated_at=invitation.traceable_time.updated_at.timestamp,
        )
