"""Schemas for a user invitation resource."""
from types import NoneType

from pydantic import BaseModel

from kwai.api.schemas.resources import UserInvitationResourceIdentifier
from kwai.core.json_api import Document, ResourceData
from kwai.modules.identity.user_invitations.user_invitation import UserInvitationEntity


class UserInvitationAttributes(BaseModel):
    """Attributes of a user invitation JSON:API resource."""

    email: str
    first_name: str
    last_name: str
    remark: str = ""
    expired_at: str | None = None
    confirmed_at: str | None = None


class UserInvitationResource(
    UserInvitationResourceIdentifier,
    ResourceData[UserInvitationAttributes, NoneType],
):
    """A JSON:API resource of a user invitation."""


class UserInvitationDocument(Document[UserInvitationResource, NoneType]):
    """A JSON:API document for one or more user invitations."""

    @classmethod
    def create(cls, user_invitation: UserInvitationEntity) -> "UserInvitationDocument":
        """Create a document for a user invitation."""
        return UserInvitationDocument(
            data=UserInvitationResource(
                id=str(user_invitation.uuid),
                attributes=UserInvitationAttributes(
                    email=str(user_invitation.email),
                    first_name=user_invitation.name.first_name,
                    last_name=user_invitation.name.last_name,
                    remark=user_invitation.remark,
                    expired_at=str(user_invitation.expired_at),
                    confirmed_at=str(user_invitation.confirmed_at)
                    if user_invitation.confirmed
                    else None,
                ),
            )
        )
