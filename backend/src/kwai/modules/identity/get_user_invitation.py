"""Implement the use case: get a user invitation."""

from dataclasses import dataclass

from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.user_invitations.user_invitation import UserInvitationEntity
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationRepository,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class GetUserInvitationCommand:
    """Input for the use case.

    [GetUserInvitation][kwai.modules.identity.get_user_invitation.GetUserInvitation]

    Attributes:
        uuid: The unique id of the user invitation.
    """

    uuid: str


class GetUserInvitation:
    """Implements the use case 'get a user invitation'."""

    def __init__(self, user_invitation_repo: UserInvitationRepository):
        """Initialize the use case.

        Args:
            user_invitation_repo: A repository for getting the user invitation.
        """
        self._user_invitation_repo = user_invitation_repo

    async def execute(self, command: GetUserInvitationCommand) -> UserInvitationEntity:
        """Execute the use case.

        Args:
            command: The input for this use case.

        Returns:
            A user invitation entity

        Raises:
            UserInvitationNotFoundException: Raised when then invitation is not found.
        """
        entity = await self._user_invitation_repo.get_invitation_by_uuid(
            UniqueId.create_from_string(command.uuid)
        )
        return entity
