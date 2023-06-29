"""Schemas for a story on a portal."""
from pydantic import BaseModel

from kwai.api.converter import MarkdownConverter
from kwai.core import json_api
from kwai.modules.news.stories.story import Application, StoryEntity


@json_api.resource(type_="applications")
class PortalApplicationResource:
    """JSON:API resource for an application."""

    def __init__(self, application: Application):
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


class StoryContent(BaseModel):
    """Schema for the content of a story."""

    locale: str
    title: str
    summary: str
    content: str | None


@json_api.resource(type_="stories")
class PortalStoryResource:
    """Represent a JSONAPI resource for a news story."""

    def __init__(self, story: StoryEntity):
        """Construct.

        Args:
            story: The story news entity that is transformed into a JSONAPI resource.
        """
        self._story = story

    @json_api.id
    def get_id(self) -> str:
        """Get the id of the story."""
        return str(self._story.id)

    @json_api.attribute(name="priority")
    def get_priority(self) -> int:
        return self._story.promotion.priority

    @json_api.attribute(name="publish_date")
    def get_publish_date(self) -> str:
        return str(self._story.period.start_date)

    @json_api.attribute(name="content")
    def get_content(self) -> list[StoryContent]:
        """Get the content of the story."""
        return [
            StoryContent(
                locale=content.locale,
                title=content.title,
                summary=MarkdownConverter().convert(content.summary),
                content=MarkdownConverter().convert(content.content)
                if content.content
                else None,
            )
            for content in self._story.content
        ]

    @json_api.relationship(name="application")
    def get_application(self) -> PortalApplicationResource:
        """Get the application of the story."""
        return PortalApplicationResource(self._story.application)
