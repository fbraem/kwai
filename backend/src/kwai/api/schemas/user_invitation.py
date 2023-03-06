"""Module that defines schema's for a user invitation."""
from pydantic import BaseModel

from kwai.core import json_api


@json_api.resource(type_="user_invitations")
class UserInvitationSchema(BaseModel):
    """The output for a user invitation."""

    id: str
    email: str
    first_name: str
    last_name: str
    remark: str
    expired_at: str
    confirmed_at: str | None
    created_at: str
    updated_at: str | None
