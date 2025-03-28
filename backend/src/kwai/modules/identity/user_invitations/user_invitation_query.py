"""Module that defines an interface for a user invitation query."""

from abc import ABC

from kwai.core.domain.repository.query import Query
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.user_invitations.user_invitation import (
    UserInvitationIdentifier,
)


class UserInvitationQuery(Query, ABC):
    """An interface for querying user invitations."""

    def filter_by_id(self, id_: UserInvitationIdentifier) -> "UserInvitationQuery":
        """Add a filter on the user invitation for id.

        Args:
            id_: An id of a user invitation.

        Returns:
            The active query
        """
        raise NotImplementedError

    def filter_by_uuid(self, uuid: UniqueId) -> "UserInvitationQuery":
        """Add a filter on the user invitation for the unique id.

        Args:
            uuid: A unique id of a user invitation.

        Returns:
            The active query
        """
        raise NotImplementedError

    def filter_by_email(self, email: EmailAddress) -> "UserInvitationQuery":
        """Add a filter on the user invitation for the email address.

        Args:
            email: An email address.

        Returns:
            The active query
        """
        raise NotImplementedError

    def filter_active(self) -> "UserInvitationQuery":
        """Add a filter to only return the active invitations at the given time.

        Returns:
            The active query
        """
        raise NotImplementedError

    def filter_not_expired(self, timestamp: Timestamp) -> "UserInvitationQuery":
        """Add a filter to only return not expired invitations.

        Returns:
            The active query.
        """
        raise NotImplementedError

    def filter_not_confirmed(self) -> "UserInvitationQuery":
        """Add a filter to only return not confirmed invitations.

        Returns:
            The active query.
        """
        raise NotImplementedError
