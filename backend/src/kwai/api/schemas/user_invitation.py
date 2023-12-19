"""Schemas for a user invitation resource."""
from types import NoneType

from pydantic import BaseModel

from kwai.core.json_api import Document, ResourceData


class UserInvitationAttributes(BaseModel):
    """Attributes of a user invitation JSON:API resource."""

    email: str
    first_name: str
    last_name: str
    remark: str
    expired_at: str | None
    confirmed_at: str | None


class UserInvitationResource(ResourceData[UserInvitationAttributes, NoneType]):
    """A JSON:API resource of a user invitation."""

    type: str = "user_invitations"


class UserInvitationDocument(Document[UserInvitationResource, NoneType]):
    """A JSON:API document for a user invitation."""
