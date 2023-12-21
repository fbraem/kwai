"""Schemas for a user invitation resource."""
from types import NoneType

from pydantic import BaseModel

from kwai.api.schemas.resources import UserInvitationResourceIdentifier
from kwai.core.json_api import Document, ResourceData


class UserInvitationAttributes(BaseModel):
    """Attributes of a user invitation JSON:API resource."""

    email: str
    first_name: str
    last_name: str
    remark: str
    expired_at: str | None
    confirmed_at: str | None


class UserInvitationResource(
    UserInvitationResourceIdentifier,
    ResourceData[UserInvitationAttributes, NoneType],
):
    """A JSON:API resource of a user invitation."""


UserInvitationDocument = Document[UserInvitationResource, NoneType]
