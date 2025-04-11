"""Schemas for a user invitation resource."""

from typing import Self

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
    mailed_at: str | None = None
    expired_at: str | None = None
    confirmed_at: str | None = None
    revoked: bool


class UserInvitationResource(
    UserInvitationResourceIdentifier,
    ResourceData[UserInvitationAttributes, None],
):
    """A JSON:API resource of a user invitation."""


class UserInvitationDocument(Document[UserInvitationResource, None]):
    """A JSON:API document for one or more user invitations."""

    @classmethod
    def create(cls, user_invitation: UserInvitationEntity) -> Self:
        """Create a document for a user invitation."""
        return cls(
            data=UserInvitationResource(
                id=str(user_invitation.uuid),
                attributes=UserInvitationAttributes(
                    email=str(user_invitation.email),
                    first_name=user_invitation.name.first_name or "",
                    last_name=user_invitation.name.last_name or "",
                    remark=user_invitation.remark,
                    mailed_at=(
                        str(user_invitation.mailed_at)
                        if user_invitation.mailed
                        else None
                    ),
                    expired_at=str(user_invitation.expired_at),
                    confirmed_at=(
                        str(user_invitation.confirmed_at)
                        if user_invitation.confirmed
                        else None
                    ),
                    revoked=user_invitation.revoked,
                ),
            )
        )
