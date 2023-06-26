"""Schemas for a user invitation resource."""

from kwai.core import json_api
from kwai.modules.identity.user_invitations.user_invitation import UserInvitationEntity


@json_api.resource(type_="user_invitations")
class UserInvitationResource:
    """Represent a JSON:API resource for a user invitation."""

    def __init__(self, invitation: UserInvitationEntity):
        self._invitation = invitation

    @json_api.id
    def get_id(self) -> str:
        """Get the id of the user invitation."""
        return str(self._invitation.uuid)

    @json_api.attribute(name="email")
    def get_email(self) -> str:
        """Get the email address for the invitation."""
        return str(self._invitation.email)

    @json_api.attribute(name="first_name")
    def get_first_name(self) -> str:
        """Get the first name of the receiver."""
        return self._invitation.name.first_name

    @json_api.attribute(name="last_name")
    def get_last_name(self) -> str:
        """Get the last name of the receiver."""
        return self._invitation.name.last_name

    @json_api.attribute(name="remark")
    def get_remark(self) -> str:
        """Get a remark about the invitation."""
        return self._invitation.remark

    @json_api.attribute(name="expired_at")
    def get_expired_at(self) -> str | None:
        """Get the timestamp of expiration."""
        return str(self._invitation.expired_at)

    @json_api.attribute(name="confirmed_at")
    def get_confirmed_at(self) -> str | None:
        """Get the timestamp of confirmation."""
        return str(self._invitation.confirmed_at)

    @json_api.attribute(name="created_at")
    def get_created_at(self) -> str | None:
        """Get the timestamp of creation."""
        return str(self._invitation.traceable_time.created_at)

    @json_api.attribute(name="updated_at")
    def get_updated_at(self) -> str | None:
        """Get the timestamp of the last update."""
        return str(self._invitation.traceable_time.updated_at)
