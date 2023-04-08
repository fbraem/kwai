"""Module that defines a user invitation entity."""
from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.users.user import UserEntity

UserInvitationIdentifier = IntIdentifier

# pylint: disable=too-many-instance-attributes


class UserInvitationEntity(Entity[UserInvitationIdentifier]):
    """A user invitation entity.

    A user invitation is a request to someone to become a member of the site.
    """

    def __init__(
        self,
        *,
        id_: UserInvitationIdentifier | None = None,
        email: EmailAddress,
        name: Name,
        uuid: UniqueId | None = None,
        expired_at: LocalTimestamp | None = None,
        remark: str = "",
        mailed_at: LocalTimestamp | None = None,
        user: UserEntity,
        confirmed_at: LocalTimestamp | None = None,
        revoked: bool = False,
        traceable_time: TraceableTime | None = None,
    ):
        """Construct a user invitation.

        Args:
            id_: The id of the user invitation.
            email: The email address that receives the invitation.
            name: The name of the invited
            uuid: The unique id to use to validate this invitation.
            expired_at: The timestamp when the invitation expires.
            remark: A remark about the invitation.
            mailed_at: The timestamp of sending out the email.
            user: The user that created the invitation.
            confirmed_at: The timestamp when the invitation was used.
            revoked: Is this invitation revoked?
            traceable_time: The creation/modification timestamp of the invitation.
        """
        super().__init__(id_ or UserInvitationIdentifier())
        self._email = email
        self._name = name
        self._uuid = uuid or UniqueId.generate()
        self._expired_at = expired_at or LocalTimestamp.create_with_delta(days=7)
        self._remark = remark
        self._mailed_at = mailed_at or LocalTimestamp()
        self._user = user
        self._confirmed_at = confirmed_at or LocalTimestamp()
        self._revoked = revoked
        self._traceable_time = traceable_time or TraceableTime()

    @property
    def email(self) -> EmailAddress:
        """Return the email address that receives this invitation."""
        return self._email

    @property
    def name(self) -> Name:
        """Return the name of the person that receives this invitation."""
        return self._name

    @property
    def uuid(self) -> UniqueId:
        """Return the unique id of this invitation."""
        return self._uuid

    @property
    def expired_at(self) -> LocalTimestamp:
        """Return when the invitation will expire."""
        return self._expired_at

    @property
    def is_expired(self) -> bool:
        """Return True when the invitation is expired."""
        return self._expired_at.is_past

    @property
    def mailed(self) -> bool:
        """Return True if the email has already been sent."""
        return not self._mailed_at.empty

    @property
    def mailed_at(self) -> LocalTimestamp:
        """Return the timestamp of sending the email."""
        return self._mailed_at

    @property
    def remark(self) -> str:
        """Return the remark about the invitation."""
        return self._remark

    @property
    def user(self) -> UserEntity:
        """Return the user that created this invitation."""
        return self._user

    def confirm(self):
        """Confirm the invitation, the invitation was used to create a new user."""
        self._confirmed_at = LocalTimestamp.create_now()
        self._traceable_time = self._traceable_time.mark_for_update()

    @property
    def confirmed(self) -> bool:
        """Return True when the invitation was confirmed."""
        return not self._confirmed_at.empty

    @property
    def confirmed_at(self) -> LocalTimestamp:
        """Return when this invitation was used."""
        return self._confirmed_at

    @property
    def revoked(self) -> bool:
        """Is this invitation revoked?."""
        return self._revoked

    @property
    def traceable_time(self) -> TraceableTime:
        """Return the creation/modification timestamp of this invitation."""
        return self._traceable_time

    def mail_sent(self):
        """Set the timestamp when the mail has been sent."""
        self._mailed_at = LocalTimestamp.create_now()
        self._traceable_time = self._traceable_time.mark_for_update()
