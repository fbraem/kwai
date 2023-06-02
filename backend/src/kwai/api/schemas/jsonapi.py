"""Module that defines some common models for JSONAPI."""
from typing import Generic, TypeVar

from fastapi import Query
from pydantic.fields import Field
from pydantic.generics import GenericModel
from pydantic.main import BaseModel

T = TypeVar("T")


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


class RelationshipData(GenericModel, Generic[T]):
    """Data for a relationship."""

    data: T


class Meta(BaseModel):
    """Defines the metadata for a document that contains a list of resources.

    Attributes:
        count: The number of actual resources
        offset: The offset of the returned resources (pagination)
        limit: The maximum number of returned resources (pagination)

    A limit of 0, means there was no limit was set.
    """

    count: int
    offset: int = 0
    limit: int = 0


class Document(GenericModel, Generic[T]):
    """A document for a single resource."""

    data: T


class Documents(GenericModel, Generic[T]):
    """A document for a single resource."""

    meta: Meta | None
    data: list[T] = Field(default_factory=list)
