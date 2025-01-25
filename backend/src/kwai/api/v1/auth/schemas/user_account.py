"""Schemas for a user account resource."""

from typing import Self

from pydantic import BaseModel

from kwai.api.v1.auth.schemas.resources import UserAccountResourceIdentifier
from kwai.core.json_api import Document, ResourceData
from kwai.modules.identity.users.user_account import UserAccountEntity


class UserAccountAttributes(BaseModel):
    """Attributes of a user account JSON:API resource."""

    email: str
    last_login: str | None
    last_unsuccessful_login: str | None
    revoked: bool
    admin: bool
    first_name: str
    last_name: str
    remark: str


class UserAccountResource(
    UserAccountResourceIdentifier, ResourceData[UserAccountAttributes, None]
):
    """A JSON:API resource for a user account."""


class UserAccountDocument(Document[UserAccountResource, None]):
    """A JSON:API document for a user account."""

    @classmethod
    def create(cls, user_account: UserAccountEntity) -> Self:
        """Create a document for a user account."""
        return cls(
            data=UserAccountResource(
                id=str(user_account.user.uuid),
                attributes=UserAccountAttributes(
                    email=str(user_account.user.email),
                    last_login=None
                    if user_account.last_login.empty
                    else str(user_account.last_login),
                    last_unsuccessful_login=None
                    if user_account.last_unsuccessful_login.empty
                    else str(user_account.last_unsuccessful_login),
                    revoked=user_account.revoked,
                    admin=user_account.admin,
                    first_name=user_account.user.name.first_name,
                    last_name=user_account.user.name.last_name,
                    remark=user_account.user.remark,
                ),
            )
        )
