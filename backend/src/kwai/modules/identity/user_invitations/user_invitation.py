"""Module that defines a user invitation entity."""

from dataclasses import dataclass, field, replace
from typing import ClassVar, Self, Type

from kwai.core.domain.entity import DataclassEntity
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.users.user import UserEntity


UserInvitationIdentifier = IntIdentifier


@dataclass(kw_only=True, eq=False, slots=True, frozen=True)
class UserInvitationEntity(DataclassEntity):
    """A user invitation entity.

    A user invitation is a request to someone to become a member of the site.

    Attributes:
        email: The email address that receives the invitation.
        name: The name of the invited
        uuid: The unique id to use to validate this invitation.
        expired_at: The timestamp when the invitation expires.
        remark: A remark about the invitation.
        mailed_at: The timestamp of sending out the email.
        user: The user that created the invitation.
        confirmed_at: The timestamp when the invitation was used.
        revoked: Is this invitation revoked?
    """

    ID: ClassVar[Type] = UserInvitationIdentifier

    email: EmailAddress
    name: Name
    uuid: UniqueId = field(default_factory=UniqueId.generate)
    expired_at: Timestamp = field(
        default_factory=lambda: Timestamp.create_with_delta(days=7)
    )
    remark: str = ""
    mailed_at: Timestamp = field(default_factory=Timestamp)
    user: UserEntity
    confirmed_at: Timestamp = field(default_factory=Timestamp)
    revoked: bool = False

    @property
    def is_expired(self) -> bool:
        """Return True when the invitation is expired."""
        return self.expired_at.is_past

    @property
    def mailed(self) -> bool:
        """Return True if the email has already been sent."""
        return not self.mailed_at.empty

    def confirm(self) -> Self:
        """Confirm the invitation, the invitation was used to create a new user.

        Returns:
            A confirmed user invitation.
        """
        return replace(
            self,
            confirmed_at=Timestamp.create_now(),
            traceable_time=self.traceable_time.mark_for_update(),
        )

    @property
    def confirmed(self) -> bool:
        """Return True when the invitation was confirmed."""
        return not self.confirmed_at.empty

    def mail_sent(self) -> Self:
        """Set the timestamp when the mail has been sent.

        Returns:
            A user invitation with a mail sent timestamp.
        """
        return replace(
            self,
            mailed_at=Timestamp.create_now(),
            traceable_time=self.traceable_time.mark_for_update(),
        )
