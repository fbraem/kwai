"""Schemas for a news item on a portal."""
from pydantic import BaseModel

from kwai.api.converter import MarkdownConverter
from kwai.core import json_api
from kwai.modules.portal.applications.application import ApplicationEntity
from kwai.modules.portal.news.news_item import NewsItemEntity


@json_api.resource(type_="applications")
class PortalApplicationResource:
    """JSON:API resource for an application."""

    def __init__(self, application: ApplicationEntity):
        self._application = application

    @json_api.id
    def get_id(self) -> str:
        """Get the id."""
        return str(self._application.id)

    @json_api.attribute(name="name")
    def get_name(self) -> str:
        """Get the name of the application."""
        return self._application.name

    @json_api.attribute(name="title")
    def get_title(self) -> str:
        """Get the title of the application."""
        return self._application.title


class NewsItemText(BaseModel):
    """Schema for the text of a news item."""

    locale: str
    title: str
    summary: str
    content: str | None


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

    @json_api.attribute(name="texts")
    def get_texts(self) -> list[NewsItemText]:
        """Get the text of the news item."""
        return [
            NewsItemText(
                locale=text.locale.value,
                title=text.title,
                summary=MarkdownConverter().convert(text.summary),
                content=MarkdownConverter().convert(text.content)
                if text.content
                else None,
            )
            for text in self._news_item.texts
        ]

    @json_api.relationship(name="application")
    def get_application(self) -> PortalApplicationResource:
        """Get the application of the news item."""
        return PortalApplicationResource(self._news_item.application)
