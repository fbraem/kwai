"""Implement the use case: delete a user invitation."""

from dataclasses import dataclass

from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationRepository,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class DeleteUserInvitationCommand:
    """Input for the use case.

    [DeleteUserInvitation][kwai.modules.identity.delete_user_invitation.DeleteUserInvitation]

    Attributes:
        uuid: The unique id of the user invitation.
    """

    uuid: str


class DeleteUserInvitation:
    """Implements the use case 'delete a user invitation'."""

    def __init__(self, user_invitation_repo: UserInvitationRepository):
        """Initialize the use case.

        Args:
            user_invitation_repo: A repository for deleting the user invitation.
        """
        self._user_invitation_repo = user_invitation_repo

    async def execute(self, command: DeleteUserInvitationCommand):
        """Execute the use case.

        Args:
            command: The input for this use case.

        Raises:
            UserInvitationNotFoundException: Raised when then invitation is not found.
        """
        entity = await self._user_invitation_repo.get_invitation_by_uuid(
            UniqueId.create_from_string(command.uuid)
        )
        await self._user_invitation_repo.delete(entity)
