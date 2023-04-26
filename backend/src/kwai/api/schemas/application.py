"""Schemas for an application resource."""
from typing import Literal

from pydantic import BaseModel, Field

from kwai.api.schemas.jsonapi import Meta


class ApplicationResourceIdentifier(BaseModel):
    """The identifier for an application resource."""

    type: Literal["applications"] = "applications"
    id: str | None


class ApplicationAttributes(BaseModel):
    """Attributes for an application resource."""

    name: str
    title: str
    description: str
    short_description: str
    remark: str = ""
    news: bool
    pages: bool
    events: bool
    weight: int
    created_at: str | None = None
    updated_at: str | None = None


class ApplicationData(ApplicationResourceIdentifier):
    """Data of the application resource."""

    attributes: ApplicationAttributes


class ApplicationDocument(BaseModel):
    """Document for one application resource."""

    data: ApplicationData


class ApplicationsDocument(BaseModel):
    """Document for a list of application resources."""

    meta: Meta | None
    data: list[ApplicationData] = Field(default_factory=list)
