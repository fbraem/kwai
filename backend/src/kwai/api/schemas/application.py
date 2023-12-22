"""Schemas for an application resource."""
from types import NoneType

from pydantic import BaseModel

from kwai.api.schemas.resources import ApplicationResourceIdentifier
from kwai.core.json_api import Document, ResourceData


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


ApplicationDocument = Document[ApplicationResource, NoneType]
