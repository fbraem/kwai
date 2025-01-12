"""Schemas for an application resource."""

from types import NoneType

from pydantic import BaseModel

from kwai.api.schemas.resources import ApplicationResourceIdentifier
from kwai.core.json_api import Document, ResourceData, ResourceMeta
from kwai.modules.portal.applications.application import ApplicationEntity


class ApplicationBaseAttributes(BaseModel):
    """Common attributes of an application JSON:API resource."""

    name: str
    title: str


class ApplicationAttributes(ApplicationBaseAttributes):
    """Attributes for an application JSON:API resource."""

    short_description: str
    description: str
    remark: str
    news: bool
    events: bool
    pages: bool
    weight: int


class ApplicationResource(
    ApplicationResourceIdentifier, ResourceData[ApplicationAttributes, NoneType]
):
    """A JSON:API resource for an application."""


class ApplicationDocument(Document[ApplicationResource, NoneType]):
    """A JSON:API document for one or more applications."""

    @classmethod
    def create(cls, application: ApplicationEntity) -> "ApplicationDocument":
        """Create a document from an application entity."""
        return ApplicationDocument(
            data=ApplicationResource(
                id=str(application.id),
                meta=ResourceMeta(
                    created_at=str(application.traceable_time.created_at),
                    updated_at=str(application.traceable_time.created_at),
                ),
                attributes=ApplicationAttributes(
                    name=application.name,
                    title=application.title,
                    short_description=application.short_description,
                    description=application.description,
                    remark=application.remark,
                    news=application.can_contain_news,
                    events=application.can_contain_events,
                    pages=application.can_contain_pages,
                    weight=application.weight,
                ),
            )
        )
