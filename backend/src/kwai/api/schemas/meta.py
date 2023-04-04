"""Module for the metamodel."""
from pydantic.main import BaseModel


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
