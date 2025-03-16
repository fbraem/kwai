"""Module that defines an interface for an invitation repository."""

from abc import ABC, abstractmethod
from typing import AsyncIterator

from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.user_invitations.user_invitation import (
    UserInvitationEntity,
    UserInvitationIdentifier,
)
from kwai.modules.identity.user_invitations.user_invitation_query import (
    UserInvitationQuery,
)


class UserInvitationNotFoundException(Exception):
    """Raised when the invitation could not be found."""


class UserInvitationRepository(ABC):
    """An invitation repository interface."""

    @abstractmethod
    def create_query(self) -> UserInvitationQuery:
        """Create a UserInvitationQuery.

        Returns:
            A query for user invitations.
        """
        raise NotImplementedError

    @abstractmethod
    def get_all(
        self,
        query: UserInvitationQuery,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncIterator[UserInvitationEntity]:
        """Return all user invitations from the query.

        Args:
            query: The prepared query.
            limit: The maximum number of entities to return.
            offset: Skip the offset rows before beginning to return entities.

        Yields:
            A list of user invitation entities.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_invitation_by_id(
        self, id_: UserInvitationIdentifier
    ) -> UserInvitationEntity:
        """Get an invitation using the id.

        Args:
            id_: The id of the invitation to search for.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_invitation_by_uuid(self, uuid: UniqueId) -> UserInvitationEntity:
        """Get an invitation using the unique id.

        Args:
            uuid: The unique id to use for searching the invitation.
        """
        raise NotImplementedError

    @abstractmethod
    async def create(self, invitation: UserInvitationEntity) -> UserInvitationEntity:
        """Create a new invitation.

        Args:
            invitation: The invitation to create.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, invitation: UserInvitationEntity) -> None:
        """Update an existing invitation.

        Args:
            invitation: The invitation to update.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, invitation: UserInvitationEntity) -> None:
        """Delete the invitation.

        Args:
            invitation: The invitation to delete.
        """
        raise NotImplementedError
