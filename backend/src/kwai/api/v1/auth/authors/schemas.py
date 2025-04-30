"""Module for defining schemas for an author resource."""

from typing import Literal, Self, TypeAlias

from pydantic import BaseModel

from kwai.core.json_api import (
    MultipleDocument,
    ResourceData,
    ResourceIdentifier,
    ResourceMeta,
    SingleDocument,
)
from kwai.modules.portal.domain.author import AuthorEntity


class AuthorResourceIdentifier(ResourceIdentifier):
    """A JSON:API resource identifier for an author."""

    type: Literal["authors"] = "authors"


class AuthorAttributes(BaseModel):
    """Attributes for an author."""

    name: str
    remark: str
    active: bool
    editor: bool


class AuthorResource(AuthorResourceIdentifier, ResourceData[AuthorAttributes, None]):
    """A JSON:API resource for an author."""

    @classmethod
    def create(cls, author: AuthorEntity) -> Self:
        """Create a JSON:API resource for an author."""
        return cls(
            id=str(author.uuid),
            attributes=AuthorAttributes(
                name=author.name,
                remark=author.remark,
                active=author.active,
                editor=author.editor,
            ),
            meta=ResourceMeta(
                created_at=str(author.traceable_time.created_at),
                updated_at=None
                if author.traceable_time.updated_at
                else str(author.traceable_time.updated_at),
            ),
        )


AuthorDocument: TypeAlias = SingleDocument[AuthorResource, None]
AuthorsDocument: TypeAlias = MultipleDocument[AuthorResource, None]
