"""Schemas for a news item."""
from types import NoneType

from pydantic import BaseModel

from kwai.api.schemas.application import ApplicationBaseAttributes
from kwai.api.schemas.resources import (
    ApplicationResourceIdentifier,
    NewsItemResourceIdentifier,
)
from kwai.core.json_api import Document, Relationship, ResourceData


class NewsItemText(BaseModel):
    """Schema for the text of a news item."""

    locale: str
    format: str
    title: str
    summary: str
    content: str | None = None
    original_summary: str
    original_content: str | None = None


class NewsItemAttributes(BaseModel):
    """Attributes of a news item JSON:API resource."""

    priority: int = 0
    publish_date: str
    end_date: str | None = None
    enabled: bool = False
    remark: str = ""
    promotion_end_date: str | None = None
    texts: list[NewsItemText]


class NewsItemRelationships(BaseModel):
    """Relationships of a news item JSON:API resource."""

    application: Relationship[ApplicationResourceIdentifier]


class NewsItemResource(
    NewsItemResourceIdentifier, ResourceData[NewsItemAttributes, NewsItemRelationships]
):
    """A JSON:API resource for a news item."""


class NewsItemApplicationResource(
    ApplicationResourceIdentifier, ResourceData[ApplicationBaseAttributes, NoneType]
):
    """A JSON:API resource for an application associated with a page."""


NewsItemDocument = Document[NewsItemResource, NewsItemApplicationResource]
