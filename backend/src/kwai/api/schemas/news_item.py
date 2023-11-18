"""Schemas for a news item."""
from pydantic import BaseModel

from kwai.api.converter import MarkdownConverter
from kwai.api.schemas.application import ApplicationResource
from kwai.core import json_api
from kwai.modules.portal.news.news_item import NewsItemEntity


class NewsItemText(BaseModel):
    """Schema for the text of a news item."""

    locale: str
    format: str
    title: str
    summary: str
    content: str | None
    original_summary: str
    original_content: str | None


@json_api.resource(type_="news_items")
class NewsItemResource:
    """Represent a JSONAPI resource for a news item."""

    def __init__(self, news_item: NewsItemEntity):
        """Construct.

        Args:
            news_item: The news item entity that is transformed into a JSONAPI resource.
        """
        self._news_item = news_item

    @json_api.id
    def get_id(self) -> str:
        """Get the id of the news item."""
        return str(self._news_item.id)

    @json_api.attribute(name="priority")
    def get_priority(self) -> int:
        """Get the priority of the promotion."""
        return self._news_item.promotion.priority

    @json_api.attribute(name="publish_date")
    def get_publish_date(self) -> str:
        """Get the publication date."""
        return str(self._news_item.period.start_date)

    @json_api.attribute(name="end_date")
    def get_end_date(self) -> str | None:
        """Get the publication end date."""
        if self._news_item.period.endless:
            return None
        return str(self._news_item.period.end_date)

    @json_api.relationship(name="application")
    def get_application(self) -> ApplicationResource:
        """Get the application of the news item."""
        return ApplicationResource(self._news_item.application)

    @json_api.attribute(name="enabled")
    def get_enabled(self) -> bool:
        """Is the news item enabled?"""
        return self._news_item.is_enabled

    @json_api.attribute(name="remark")
    def get_remark(self) -> str:
        """Get the remark of the news item."""
        return self._news_item.remark or ""

    @json_api.attribute(name="promotion_end_date")
    def get_promotion_end_date(self) -> str | None:
        """Get the publication end date."""
        if self._news_item.promotion.end_date.empty:
            return None
        return str(self._news_item.period.end_date)

    @json_api.attribute(name="texts")
    def get_texts(self) -> list[NewsItemText]:
        """Get the text of the news item."""
        return [
            NewsItemText(
                format=text.format.value,
                title=text.title,
                summary=MarkdownConverter().convert(text.summary),
                content=MarkdownConverter().convert(text.content)
                if text.content
                else None,
                locale=text.locale.value,
                original_summary=text.summary,
                original_content=text.content,
            )
            for text in self._news_item.texts
        ]
