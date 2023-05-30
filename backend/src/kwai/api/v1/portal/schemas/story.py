"""Schemas for a story on a portal."""
from typing import Literal

from pydantic import BaseModel, Field

from kwai.api.schemas.jsonapi import Meta


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

    content: list[PortalStoryContent]
    publish_date: str
    promotion: int


class PortalStoryData(PortalStoryResourceIdentifier):
    """Data of a story on a portal."""

    attributes: PortalStoryAttributes


class PortalStoryDocument(BaseModel):
    """Document for a story on a portal."""

    data: PortalStoryData


class PortalStoriesDocument(BaseModel):
    """Document for a list of stories on a portal."""

    meta: Meta | None
    data: list[PortalStoryData] = Field(default_factory=list)
