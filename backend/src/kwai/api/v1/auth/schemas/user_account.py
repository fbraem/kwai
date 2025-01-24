"""Schemas for a user account resource."""

from typing import Self

from pydantic import BaseModel

from kwai.api.v1.auth.schemas.resources import UserAccountResourceIdentifier
from kwai.core.json_api import Document, ResourceData
from kwai.modules.identity.users.user_account import UserAccountEntity


class UserAccountAttributes(BaseModel):
    """Attributes of a user account JSON:API resource."""

    email: str


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
                id=str(user_account.id),
                attributes=UserAccountAttributes(email=str(user_account.user.email)),
            )
        )
