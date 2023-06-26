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
        return str(self._application.id)

    @json_api.attribute(name="name")
    def get_name(self) -> str:
        return self._application.name

    @json_api.attribute(name="name")
    def get_title(self) -> str:
        return self._application.title

    @json_api.attribute(name="name")
    def get_description(self) -> str:
        return self._application.description

    @json_api.attribute(name="name")
    def get_short_description(self) -> str:
        return self._application.short_description

    @json_api.attribute(name="name")
    def get_remark(self) -> str:
        return self._application.remark

    @json_api.attribute(name="name")
    def get_news(self) -> bool:
        return self._application.can_contain_news

    @json_api.attribute(name="name")
    def get_pages(self) -> bool:
        return self._application.can_contain_pages

    @json_api.attribute(name="name")
    def get_events(self) -> bool:
        return self._application.can_contain_events

    @json_api.attribute(name="name")
    def get_weight(self) -> int:
        return self._application.weight

    @json_api.attribute(name="name")
    def get_created_at(self) -> str:
        return str(self._application.traceable_time.created_at)

    @json_api.attribute(name="name")
    def get_updated_at(self) -> str:
        return str(self._application.traceable_time.updated_at)
