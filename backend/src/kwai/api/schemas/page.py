"""Module for defining the page JSON:API resource."""
from pydantic import BaseModel

from kwai.api.converter import MarkdownConverter
from kwai.api.schemas.application import ApplicationResource
from kwai.core import json_api
from kwai.modules.portal.pages.page import PageEntity


class PageText(BaseModel):
    """Schema for the text of a page."""

    locale: str
    format: str
    title: str
    summary: str
    content: str | None


@json_api.resource(type_="pages")
class PageResource:
    """JSON:API resource for a page entity."""

    def __init__(self, page_entity: PageEntity):
        self._page = page_entity

    @json_api.id
    def get_id(self) -> str:
        """Get the id of the page."""
        return str(self._page.id)

    @json_api.attribute(name="enabled")
    def is_enabled(self) -> bool:
        """Return the enabled attribute of the page."""
        return self._page.enabled

    @json_api.attribute(name="priority")
    def get_priority(self) -> int:
        """Return the priority attribute of the page."""
        return self._page.priority

    @json_api.attribute(name="remark")
    def get_remark(self) -> str:
        """Return the remark attribute of the page."""
        return self._page.remark or ""

    @json_api.relationship(name="application")
    def get_application(self) -> ApplicationResource:
        """Return the application relationship."""
        return ApplicationResource(self._page.application)

    @json_api.attribute(name="texts")
    def get_texts(self) -> list[PageText]:
        """Get the text of the news item."""
        return [
            PageText(
                locale=text.locale.value,
                format=text.format.value,
                title=text.title,
                summary=MarkdownConverter().convert(text.summary),
                content=MarkdownConverter().convert(text.content)
                if text.content
                else None,
            )
            for text in self._page.texts
        ]
