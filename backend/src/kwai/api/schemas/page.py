"""Module for defining the page JSON:API resource."""
from types import NoneType

from pydantic import BaseModel

from kwai.api.schemas.application import ApplicationBaseAttributes
from kwai.api.schemas.resources import (
    ApplicationResourceIdentifier,
    PageResourceIdentifier,
)
from kwai.core.json_api import Document, Relationship, ResourceData


class PageText(BaseModel):
    """Schema for the text of a page."""

    locale: str
    format: str
    title: str
    summary: str
    content: str | None
    original_summary: str
    original_content: str | None


class PageAttributes(BaseModel):
    """Attributes of a page JSON:API resource."""

    enabled: bool
    priority: int
    remark: str
    texts: list[PageText]


class PageRelationships(BaseModel):
    """Relationships of a page JSON:API resource."""

    application: Relationship[ApplicationResourceIdentifier]


class PageResource(
    PageResourceIdentifier, ResourceData[PageAttributes, PageRelationships]
):
    """A JSON:API resource for a page."""


class PageApplicationResource(
    ApplicationResourceIdentifier, ResourceData[ApplicationBaseAttributes, NoneType]
):
    """A JSON:API resource for an application associated with a page."""


PageDocument = Document[PageResource, PageApplicationResource]
