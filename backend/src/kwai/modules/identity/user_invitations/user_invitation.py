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

    Attributes
    ----------
        _email(EmailAddress): The email address that receives the invitation.
        _name(Name): The name of the invited
        _uuid(UniqueId): The unique id to use to validate this invitation.
        _expired_at(LocalTimestamp): The timestamp when the invitation expires.
        _remark(str): A remark about the invitation
        _user(UserEntity): The user that created the invitation
        _confirmed_at(LocalTimestamp): The timestamp when the invitation was used
        _revoked(bool): Is this invitation revoked?
        _traceable_time(TraceableTime): The creation/modification timestamp of the
            invitation.

    Note:
        All attributes are by default private. Properties are defined for getting
        the values.
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
        user: UserEntity,
        confirmed_at: LocalTimestamp | None = None,
        revoked: bool = False,
        traceable_time: TraceableTime | None = None,
    ):
        super().__init__(id_ or UserInvitationIdentifier())
        self._email = email
        self._name = name
        self._uuid = uuid or UniqueId.generate()
        self._expired_at = expired_at or LocalTimestamp.create_with_delta(days=7)
        self._remark = remark
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
    def remark(self) -> str:
        """Return the remark about the invitation."""
        return self._remark

    @property
    def user(self) -> UserEntity:
        """Return the user that created this invitation."""
        return self._user

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
