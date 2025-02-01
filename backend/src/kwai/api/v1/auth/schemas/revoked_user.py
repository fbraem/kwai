"""Schemas for a revoked user."""

from pydantic import BaseModel

from kwai.api.v1.auth.schemas.resources import RevokedUserResourceIdentifier
from kwai.core.json_api import Document, ResourceData
from kwai.modules.identity.users.user_account import UserAccountEntity


class RevokedUserAttributes(BaseModel):
    """Attributes for a revoked user."""

    revoked: bool


class RevokedUserResource(
    RevokedUserResourceIdentifier, ResourceData[RevokedUserAttributes, None]
):
    """A JSON:API resource for a revoked user."""


class RevokedUserDocument(Document[RevokedUserResource, None]):
    """A JSON:API document for a revoked user."""

    @classmethod
    def create(cls, user_account: UserAccountEntity):
        """Create a revoked user document."""
        return cls(
            data=RevokedUserResource(
                id=str(user_account.user.uuid),
                attributes=RevokedUserAttributes(revoked=user_account.revoked),
            )
        )
