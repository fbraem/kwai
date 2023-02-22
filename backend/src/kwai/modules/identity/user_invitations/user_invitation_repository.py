"""Module that defines an interface for an invitation repository."""
from abc import ABC

from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.user_invitations.user_invitation import (
    UserInvitationIdentifier,
    UserInvitationEntity,
)


class UserInvitationNotFoundException(Exception):
    """Raised when the invitation could not be found."""


class UserInvitationRepository(ABC):
    """An invitation repository interface."""

    def get_invitation_by_id(
        self, id_: UserInvitationIdentifier
    ) -> UserInvitationEntity:
        """Get an invitation using the id.

        Args:
            id_(UserInvitationIdentifier): The id of the invitation to search for.
        """
        raise NotImplementedError

    def get_invitation_by_uuid(self, uuid: UniqueId) -> UserInvitationEntity:
        """Get an invitation using the uniqued id.

        Args:
            uuid(UniqueId): The unique id to use for searching the invitation.
        """
        raise NotImplementedError

    def create(self, invitation: UserInvitationEntity) -> UserInvitationEntity:
        """Creates a new invitation.

        Args:
            invitation(UserInvitationEntity): The invitation to create.
        """
        raise NotImplementedError

    def update(self, invitation: UserInvitationEntity) -> None:
        """Updates an existing invitation.

        Args:
            invitation(UserInvitationEntity): The invitation to update.
        """
        raise NotImplementedError

    def delete(self, invitation: UserInvitationEntity) -> None:
        """Deletes the invitation.

        Args:
            invitation(UserInvitationEntity): The invitation to delete.
        """
        raise NotImplementedError
