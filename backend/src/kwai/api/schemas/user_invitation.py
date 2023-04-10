"""Schemas for a user invitation resource."""
from typing import Literal

from pydantic import BaseModel, Field

from kwai.api.schemas.jsonapi import Meta


class UserInvitationResourceIdentifier(BaseModel):
    """The identifier for a user invitation resource."""

    type: Literal["user_invitations"] = "user_invitations"
    id: str | None


class UserInvitationAttributes(BaseModel):
    """Attributes for a user invitation resource."""

    email: str
    first_name: str
    last_name: str
    remark: str = ""
    expired_at: str | None = None
    confirmed_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class UserInvitationData(UserInvitationResourceIdentifier):
    """Data of the user invitation resource."""

    attributes: UserInvitationAttributes


class UserInvitationDocument(BaseModel):
    """Document for one user invitation resource."""

    data: UserInvitationData


class UserInvitationsDocument(BaseModel):
    """Document for a list of user invitation resources."""

    meta: Meta | None
    data: list[UserInvitationData] = Field(default_factory=list)
