"""Schemas for a news item."""

from types import NoneType

from pydantic import BaseModel

from kwai.api.converter import MarkdownConverter
from kwai.api.schemas.application import ApplicationBaseAttributes
from kwai.api.schemas.resources import (
    ApplicationResourceIdentifier,
    NewsItemResourceIdentifier,
)
from kwai.core.json_api import Document, Relationship, ResourceData, ResourceMeta
from kwai.modules.portal.news.news_item import NewsItemEntity


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


class NewsItemDocument(Document[NewsItemResource, NewsItemApplicationResource]):
    """A JSON:API document for one or more news items."""

    @classmethod
    def create(cls, news_item: NewsItemEntity) -> "NewsItemDocument":
        """Create a document from a news item entity."""
        data = NewsItemResource(
            id=str(news_item.id),
            meta=ResourceMeta(
                created_at=str(news_item.traceable_time.created_at),
                updated_at=str(news_item.traceable_time.updated_at),
            ),
            attributes=NewsItemAttributes(
                priority=news_item.promotion.priority,
                publish_date=str(news_item.period.start_date),
                end_date=str(news_item.period.end_date),
                enabled=news_item.is_enabled,
                remark=news_item.remark or "",
                promotion_end_date=str(news_item.promotion.end_date),
                texts=[
                    NewsItemText(
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
                    for text in news_item.texts
                ],
            ),
            relationships=NewsItemRelationships(
                application=Relationship[ApplicationResourceIdentifier](
                    data=ApplicationResourceIdentifier(id=str(news_item.application.id))
                )
            ),
        )

        included = {
            NewsItemApplicationResource(
                id=str(news_item.application.id),
                attributes=ApplicationBaseAttributes(
                    name=news_item.application.name, title=news_item.application.title
                ),
            )
        }

        return NewsItemDocument(data=data, included=included)
