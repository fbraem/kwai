"""Module for implementing the use case of recreating a user invitation."""

from dataclasses import dataclass

from kwai.core.domain.exceptions import UnprocessableException
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


@dataclass(kw_only=True, slots=True, frozen=True)
class RecreateUserInvitationCommand:
    """Input for the use case 'Recreate User Invitation'.

    [RecreateUserInvitation][kwai.modules.identity.invite_user.RecreateUserInvitation]

    Attributes:
        uuid: The unique id of the original invitation.
        expiration_in_days: When does the invitation expires (in days)
        remark: A remark for this user invitation
    """

    uuid: str
    expiration_in_days: int = 7
    remark: str = ""


class RecreateUserInvitation:
    """Use case for recreating a user invitation."""

    def __init__(
        self,
        user: UserEntity,
        user_repo: UserRepository,
        user_invitation_repo: UserInvitationRepository,
        publisher: Publisher,
    ):
        """Initialize the use case."""
        self._user = user
        self._user_repo = user_repo
        self._user_invitation_repo = user_invitation_repo
        self._publisher = publisher

    async def execute(
        self, command: RecreateUserInvitationCommand
    ) -> UserInvitationEntity:
        """Execute the use case.

        Args:
            command: The input for this use case.

        Returns:
            A user invitation.

        Raises:
            UnprocessableException: raised when the email address is already in use.
        """
        uuid = UniqueId.create_from_string(command.uuid)
        original_invitation = await self._user_invitation_repo.get_invitation_by_uuid(
            uuid
        )
        original_invitation = original_invitation.revoke()
        await self._user_invitation_repo.update(original_invitation)

        try:
            await self._user_repo.get_user_by_email(original_invitation.email)
            raise UnprocessableException(
                f"{original_invitation.email} is already in use"
            )
        except UserNotFoundException:
            pass

        query = (
            self._user_invitation_repo.create_query()
            .filter_by_email(original_invitation.email)
            .filter_active(Timestamp.create_now())
        )
        if await query.count() > 0:
            raise UnprocessableException(
                f"There are still pending invitations for {original_invitation.email}"
            )

        invitation = await self._user_invitation_repo.create(
            UserInvitationEntity(
                email=original_invitation.email,
                name=original_invitation.name,
                uuid=UniqueId.generate(),
                expired_at=Timestamp.create_with_delta(days=command.expiration_in_days),
                remark=command.remark,
                user=self._user,
            )
        )

        await self._publisher.publish(
            UserInvitationCreatedEvent(uuid=str(invitation.uuid))
        )

        return invitation
