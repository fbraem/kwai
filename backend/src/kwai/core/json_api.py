"""Module that defines some JSON:API related models."""

from typing import Any, Generic, TypeVar, cast

from fastapi import Query
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    GetJsonSchemaHandler,
    model_serializer,
)
from pydantic.json_schema import JsonSchemaValue, SkipJsonSchema
from pydantic_core import CoreSchema


class ResourceIdentifier(BaseModel):
    """A JSON:API resource identifier."""

    id: str | SkipJsonSchema[None] = None
    type: str

    def __hash__(self) -> int:
        """Create a hash for a resource."""
        return hash(str(self.id) + self.type)


T_RELATION_SHIP = TypeVar("T_RELATION_SHIP")


class Relationship(BaseModel, Generic[T_RELATION_SHIP]):
    """A JSON:API relationship."""

    data: T_RELATION_SHIP | list[T_RELATION_SHIP] | None


class ResourceMeta(BaseModel):
    """Meta for a JSON:API resource."""

    model_config = ConfigDict(extra="allow")

    created_at: str
    updated_at: str | None = None


T_ATTRS = TypeVar("T_ATTRS")
T_RELATIONSHIPS = TypeVar("T_RELATIONSHIPS")


class ResourceData(BaseModel, Generic[T_ATTRS, T_RELATIONSHIPS]):
    """A JSON:API resource."""

    meta: ResourceMeta | SkipJsonSchema[None] = None
    attributes: T_ATTRS
    relationships: T_RELATIONSHIPS | SkipJsonSchema[None] = None

    @model_serializer(mode="wrap")
    def serialize(self, handler) -> dict[str, Any]:
        """Remove relationships and meta from serialization when the values are none."""
        result = handler(self)
        if self.relationships is None:
            del result["relationships"]
        if self.meta is None:
            del result["meta"]
        return result


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


class ErrorSource(BaseModel):
    """Defines the model for an error source."""

    pointer: str


class Error(BaseModel):
    """Defines the model for a JSON:API error."""

    status: str = ""
    source: ErrorSource | None = None
    title: str = ""
    detail: str = ""


class Document(BaseModel, Generic[T_RESOURCE, T_INCLUDE]):
    """A JSON:API document."""

    meta: Meta | SkipJsonSchema[None] = None
    data: T_RESOURCE | list[T_RESOURCE]
    included: set[T_INCLUDE] | SkipJsonSchema[None] = None
    errors: list[Error] | SkipJsonSchema[None] = None

    @property
    def resource(self) -> T_RESOURCE:
        """Return the resource of this document.

        An assert will occur, when the resource is a list.
        """
        assert not isinstance(self.data, list)
        return self.data

    @property
    def resources(self) -> list[T_RESOURCE]:
        """Return the list of resources of this document.

        An assert will occur, when the resource is not a list.
        """
        assert isinstance(self.data, list)
        return self.data

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        core_schema: CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        """Remove included when T_INCLUDE is NoneType."""
        json_schema = handler(core_schema)
        json_schema = handler.resolve_ref_schema(json_schema)
        if "properties" in json_schema:
            if "type" in json_schema["properties"]["included"]["items"]:
                if json_schema["properties"]["included"]["items"]["type"] == "null":
                    del json_schema["properties"]["included"]
        return json_schema

    @model_serializer(mode="wrap")
    def serialize(self, handler) -> dict[str, Any]:
        """Remove included and meta when the value is None."""
        result = handler(self)
        if self.included is None:
            del result["included"]
        if self.meta is None:
            del result["meta"]
        if not self.errors:
            del result["errors"]
        return result

    def merge(self, other: "Document"):
        """Merge a document into this document.

        When data is not a list yet, it will be converted to a list. When there are
        included resources, they will be merged into this document.
        meta is not merged.
        """
        if not isinstance(self.data, list):
            self.data = [self.data]
        self.data.append(cast(Any, other.data))
        if other.included is not None:
            if self.included is None:
                self.included = other.included
            else:
                self.included = self.included.union(other.included)


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


class JsonApiPresenter[Document]:
    """An interface for a presenter that generates a JSON:API document."""

    def __init__(self):
        self._document: Document = None

    def get_document(self) -> Document:
        """Return the JSON:API document."""
        return self._document
