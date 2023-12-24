"""Module for defining the page JSON:API resource."""
from types import NoneType

from pydantic import BaseModel

from kwai.api.converter import MarkdownConverter
from kwai.api.schemas.application import ApplicationBaseAttributes
from kwai.api.schemas.resources import (
    ApplicationResourceIdentifier,
    PageResourceIdentifier,
)
from kwai.core.json_api import Document, Relationship, ResourceData, ResourceMeta
from kwai.modules.portal.pages.page import PageEntity


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


class PageDocument(Document[PageResource, PageApplicationResource]):
    """A JSON:API document for one or more pages."""

    @classmethod
    def create(cls, page: PageEntity):
        """Create a document from a page entity."""
        data = PageResource(
            id=str(page.id),
            meta=ResourceMeta(
                created_at=str(page.traceable_time.created_at),
                updated_at=str(page.traceable_time.updated_at),
            ),
            attributes=PageAttributes(
                enabled=page.enabled,
                priority=page.priority,
                remark=page.remark or "",
                texts=[
                    PageText(
                        locale=text.locale.value,
                        format=text.format.value,
                        title=text.title,
                        summary=MarkdownConverter().convert(text.summary),
                        content=MarkdownConverter().convert(text.content)
                        if text.content
                        else None,
                        original_summary=text.summary,
                        original_content=text.content,
                    )
                    for text in page.texts
                ],
            ),
            relationships=PageRelationships(
                application=Relationship[ApplicationResourceIdentifier](
                    data=ApplicationResourceIdentifier(id=str(page.application.id))
                )
            ),
        )
        included = {
            PageApplicationResource(
                id=str(page.application.id),
                attributes=ApplicationBaseAttributes(
                    name=page.application.name, title=page.application.title
                ),
            )
        }

        return PageDocument(data=data, included=included)
