"""Implement the use case: get user invitations."""
from dataclasses import dataclass
from typing import AsyncIterator

from kwai.modules.identity.user_invitations.user_invitation import UserInvitationEntity
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationRepository,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class GetInvitationsCommand:
    """Input for the use case.

    [GetInvitations][kwai.modules.identity.get_invitations.GetInvitations]

    Attributes:
        offset: Offset to use. Default is None.
        limit: The max. number of elements to return. Default is None, which means all.
    """

    offset: int | None = None
    limit: int | None = None


class GetInvitations:
    """Implementation of the use case.

    Use this use case for getting user invitations.
    """

    def __init__(self, user_invitation_repo: UserInvitationRepository):
        """Initialize the use case.

        Args:
            user_invitation_repo: A repository for getting the user invitations.
        """
        self._user_invitation_repo = user_invitation_repo

    async def execute(
        self, command: GetInvitationsCommand
    ) -> tuple[int, AsyncIterator[UserInvitationEntity]]:
        """Execute the use case.

        Args:
            command: The input for this use case.

        Returns:
            A tuple with the number of entities and an iterator for invitation entities.
        """
        query = self._user_invitation_repo.create_query()
        return (
            await query.count(),
            self._user_invitation_repo.get_all(
                query=query, offset=command.offset, limit=command.limit
            ),
        )
