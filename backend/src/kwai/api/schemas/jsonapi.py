"""Module that defines some common models for JSONAPI."""
from fastapi import Query
from pydantic.fields import Field
from pydantic.main import BaseModel


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


class Meta(BaseModel):
    """Defines the metadata for a document that contains a list of resources.

    Attributes:
        count: The number of actual resources
        offset: The offset of the returned resources (pagination)
        limit: The maximum number of returned resources (pagination)
    """

    count: int
    offset: int | None
    limit: int | None
