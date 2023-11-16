"""Schemas for an application resource."""
from kwai.core import json_api
from kwai.modules.portal.applications.application import ApplicationEntity


@json_api.resource(type_="applications")
class ApplicationResource:
    """Represents a JSON:API resource for applications."""

    def __init__(self, application: ApplicationEntity):
        self._application = application

    @json_api.id
    def get_id(self) -> str:
        """Get the id of the application."""
        return str(self._application.id)

    @json_api.attribute(name="name")
    def get_name(self) -> str:
        """Get the name of the application."""
        return self._application.name

    @json_api.attribute(name="title")
    def get_title(self) -> str:
        """Get the title of the application."""
        return self._application.title

    @json_api.attribute(name="description")
    def get_description(self) -> str:
        """Get the description of the application."""
        return self._application.description

    @json_api.attribute(name="short_description")
    def get_short_description(self) -> str:
        """Get the short description the application."""
        return self._application.short_description

    @json_api.attribute(name="remark")
    def get_remark(self) -> str:
        """Get the remark about the application."""
        return self._application.remark

    @json_api.attribute(name="news")
    def get_news(self) -> bool:
        """Check if this application can contain news stories."""
        return self._application.can_contain_news

    @json_api.attribute(name="pages")
    def get_pages(self) -> bool:
        """Check if this application can contain pages."""
        return self._application.can_contain_pages

    @json_api.attribute(name="events")
    def get_events(self) -> bool:
        """Check if this application can contain events."""
        return self._application.can_contain_events

    @json_api.attribute(name="weight")
    def get_weight(self) -> int:
        """Get the weight of the application."""
        return self._application.weight

    @json_api.attribute(name="created_at")
    def get_created_at(self) -> str | None:
        """Get the timestamp of creation."""
        return str(self._application.traceable_time.created_at)

    @json_api.attribute(name="updated_at")
    def get_updated_at(self) -> str | None:
        """Get the timestamp of the last update."""
        return str(self._application.traceable_time.updated_at)
