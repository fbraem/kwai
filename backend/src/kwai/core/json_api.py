"""Module that defines some JSON:API related models."""
from typing import Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field
from pydantic.json_schema import SkipJsonSchema


class ResourceIdentifier(BaseModel):
    """A JSON:API resource identifier."""

    id: str | SkipJsonSchema[None] = None
    type: str


class Relationship(BaseModel):
    """A JSON:API relationship."""

    data: ResourceIdentifier | list[ResourceIdentifier]


class ResourceMeta(BaseModel):
    """Meta for a JSON:API resource."""

    model_config = ConfigDict(extra="allow")

    created_at: str
    updated_at: str | None = None


T_ATTRS = TypeVar("T_ATTRS")
T_RELATIONSHIP = TypeVar("T_RELATIONSHIP")


class ResourceData(ResourceIdentifier, Generic[T_ATTRS, T_RELATIONSHIP]):
    """A JSON:API resource."""

    meta: ResourceMeta | SkipJsonSchema[None] = None
    attributes: T_ATTRS
    relationships: T_RELATIONSHIP | SkipJsonSchema[None] = None


T_RESOURCE = TypeVar("T_RESOURCE")
T_INCLUDE = TypeVar("T_INCLUDE")


class Meta(BaseModel):
    """Defines the metadata for the document model.

    Attributes:
        count: The number of actual resources
        offset: The offset of the returned resources (pagination)
        limit: The maximum number of returned resources (pagination)

    A limit of 0, means there was no limit was set.
    """

    model_config = ConfigDict(extra="allow")

    count: int | None = None
    offset: int | None = None
    limit: int | None = None


class Document(BaseModel, Generic[T_RESOURCE, T_INCLUDE]):
    """A JSON:API document."""

    meta: Meta | SkipJsonSchema[None] = None
    data: T_RESOURCE | list[T_RESOURCE]
    included: T_INCLUDE | SkipJsonSchema[None] = None


class PaginationModel(BaseModel):
    """A model for pagination query parameters.

    Use this as a dependency on a route. This will handle the page[offset]
    and page[limit] query parameters.

    Attributes:
        offset: The value of the page[offset] query parameter. Default is None.
        limit: The value of the page[limit] query parameter. Default is None.
    """

    offset: int | None = Field(Query(default=None, alias="page[offset]"))
    limit: int | None = Field(Query(default=None, alias="page[limit]"))
