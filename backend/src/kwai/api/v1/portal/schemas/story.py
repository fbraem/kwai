"""Schemas for a story on a portal."""
from typing import Literal

from pydantic import BaseModel

from kwai.api.schemas.application import ApplicationResourceIdentifier
from kwai.api.schemas.jsonapi import RelationshipData, Document, Documents


class PortalStoryResourceIdentifier(BaseModel):
    """The identifier for a news story."""

    type: Literal["stories"] = "stories"
    id: str | None


class PortalStoryContent(BaseModel):
    """Schema for content of a story."""

    locale: str
    title: str
    summary: str
    content: str | None


class PortalStoryAttributes(BaseModel):
    """Attributes for a story on a portal."""

    priority: int
    content: list[PortalStoryContent]
    publish_date: str


class PortalStoryRelationships(BaseModel):
    """Relationships of a story."""

    application: RelationshipData[ApplicationResourceIdentifier]


class PortalStoryApplicationAttributes(BaseModel):
    """Attributes for an application."""

    name: str
    title: str


class PortalStoryApplicationData(ApplicationResourceIdentifier):
    """Data for an application."""

    attributes: PortalStoryApplicationAttributes

    def __hash__(self):
        return hash(self.id + "/" + self.type)


class PortalStoryData(PortalStoryResourceIdentifier):
    """Data of a story on a portal."""

    attributes: PortalStoryAttributes
    relationships: PortalStoryRelationships


# pylint: disable=too-few-public-methods


class PortalStoryDocument(Document[PortalStoryData]):
    """Document for a story on a portal."""


class PortalStoriesDocument(Documents[PortalStoryData]):
    """Document for a list of stories on a portal."""

    included: list[PortalStoryApplicationData]
