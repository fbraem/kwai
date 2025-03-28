"""Module for the invite user use case."""

from dataclasses import dataclass

from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.core.events.publisher import Publisher
from kwai.modules.identity.user_invitations.user_invitation import UserInvitationEntity
from kwai.modules.identity.user_invitations.user_invitation_events import (
    UserInvitationCreatedEvent,
)
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationRepository,
)
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.identity.users.user_repository import (
    UserNotFoundException,
    UserRepository,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class InviteUserCommand:
    """Input for the use case.

    [InviteUser][kwai.modules.identity.invite_user.InviteUser]

    Attributes:
        first_name: Firstname of the invited
        last_name: Lastname of the invited
        email: Email address of the invited
        expiration_in_days: After how many days will the invitation expire?
        remark: A remark about this invitation
    """

    first_name: str
    last_name: str
    email: str
    expiration_in_days: int = 7
    remark: str = ""


class InviteUser:
    """Invite user use case.

    This use case will try to create an invitation for a user.
    """

    def __init__(
        self,
        user: UserEntity,
        user_repo: UserRepository,
        user_invitation_repo: UserInvitationRepository,
        publisher: Publisher,
    ):
        """Initialize the use case.

        Args:
            user: The inviter.
            user_repo: The repository to check if the email address is still free.
            user_invitation_repo: The repository for creating an invitation.
            publisher: A publisher for publishing the user invitation created event.
        """
        self._user = user
        self._user_repo = user_repo
        self._user_invitation_repo = user_invitation_repo
        self._publisher = publisher

    async def execute(self, command: InviteUserCommand) -> UserInvitationEntity:
        """Execute the use case.

        Args:
            command: The input for this use case.

        Returns:
            A user invitation

        Raises:
            UnprocessableException: raised when the email address is already in use or
                when there are still pending invitations for the email address.
        """
        email_address = EmailAddress(command.email)
        try:
            await self._user_repo.get_user_by_email(email_address)
            raise UnprocessableException(f"{command.email} is already used.")
        except UserNotFoundException:
            pass

        query = (
            self._user_invitation_repo.create_query()
            .filter_by_email(email_address)
            .filter_active()
            .filter_not_expired(Timestamp.create_now())
        )
        if await query.count() > 0:
            raise UnprocessableException(
                f"There are still pending invitations for {command.email}"
            )

        invitation = await self._user_invitation_repo.create(
            UserInvitationEntity(
                email=email_address,
                name=Name(first_name=command.first_name, last_name=command.last_name),
                uuid=UniqueId.generate(),
                expired_at=Timestamp.create_with_delta(days=command.expiration_in_days),
                user=self._user,
            )
        )

        await self._publisher.publish(
            UserInvitationCreatedEvent(uuid=str(invitation.uuid))
        )

        return invitation
