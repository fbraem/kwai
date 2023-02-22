"""Module that defines an interface for an invitation repository."""
from abc import ABC
from typing import Iterator

from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.user_invitations.user_invitation import (
    UserInvitationIdentifier,
    UserInvitationEntity,
)
from kwai.modules.identity.user_invitations.user_invitation_query import (
    UserInvitationQuery,
)


class UserInvitationNotFoundException(Exception):
    """Raised when the invitation could not be found."""


class UserInvitationRepository(ABC):
    """An invitation repository interface."""

    def create_query(self) -> UserInvitationQuery:
        """Create a UserInvitationQuery.

        Returns:
            A query for user invitations.
        """
        raise NotImplementedError

    def get_all(
        self,
        query: UserInvitationQuery,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Iterator[UserInvitationEntity]:
        """Return all user invitations from the query.

        Args:
            query: The prepared query.
            limit: The maximum number of entities to return.
            offset: Skip the offset rows before beginning to return entities.

        Yields:
            A list of user invitation entities.
        """
        raise NotImplementedError

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
