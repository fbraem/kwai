"""Schemas for a user account resource."""

from typing import Self

from pydantic import BaseModel

from kwai.api.schemas.resources import UserInvitationResourceIdentifier
from kwai.api.v1.auth.schemas.resources import UserAccountResourceIdentifier
from kwai.core.json_api import (
    MultipleDocument,
    Relationship,
    ResourceData,
    SingleDocument,
)
from kwai.modules.identity.users.user_account import UserAccountEntity


class BaseUserAccountAttributes(BaseModel):
    """Base attributes for a user account JSON:API resource."""

    first_name: str
    last_name: str
    remark: str


class UserAccountAttributes(BaseUserAccountAttributes):
    """Attributes of a user account JSON:API resource."""

    email: str
    last_login: str | None
    last_unsuccessful_login: str | None
    revoked: bool
    admin: bool


class CreateUserAccountAttributes(BaseUserAccountAttributes):
    """Attributes for creating a user account."""

    password: str


class UserAccountResource(
    UserAccountResourceIdentifier, ResourceData[UserAccountAttributes, None]
):
    """A JSON:API resource for a user account."""

    @classmethod
    def create(cls, user_account: UserAccountEntity) -> Self:
        """Create a document for a user account."""
        return cls(
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


UserAccountDocument = SingleDocument[UserAccountResource, None]
UserAccountsDocument = MultipleDocument[UserAccountResource, None]


class CreateUserAccountRelationships(BaseModel):
    """Relationships needed for creating a user account."""

    user_invitation: Relationship[UserInvitationResourceIdentifier]


class CreateUserAccountResource(
    UserAccountResourceIdentifier,
    ResourceData[CreateUserAccountAttributes, CreateUserAccountRelationships],
):
    """A JSON:API resource for creating a user account."""
