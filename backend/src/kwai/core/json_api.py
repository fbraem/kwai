"""Module that defines some jsonapi related models."""
import dataclasses
from dataclasses import dataclass, field
from typing import Any, Tuple

from pydantic import BaseModel, Field, conlist


class JsonApiResourceIdentifier(BaseModel):
    """Define a JSONAPI resource identifier."""

    id: str
    type: str


class JsonApiRelationship(BaseModel):
    """Define a JSONAPI relationship."""

    data: JsonApiResourceIdentifier | list[JsonApiResourceIdentifier]


class JsonApiData(BaseModel):
    """Define a JSONAPI data."""

    id: str
    type: str
    attributes: dict[str, Any]
    relationships: dict[str, JsonApiRelationship] | None = None


class JsonApiDocument(BaseModel):
    """Define a JSONAPI document."""

    meta: dict[str, Any] | None = None
    data: JsonApiData | list[JsonApiData] = Field(default_factory=list)
    included: conlist(item_type=JsonApiData, unique_items=True) | None = None

    def json(self, *args, **kwargs) -> str:
        """
        Override the default json method to exclude None values
        """
        return super().json(*args, exclude_none=True, **kwargs)


@dataclass(kw_only=True)
class Resource:
    """Class that collects all information of the jsonapi decorators used in a class.

    Attributes:
        type: The type of the resource.
        id: The method/property to use to get the id of a resource.
        attributes: A dictionary of methods to get all attributes of a resource.
        relationships: A dictionary of methods to get all related resources of a
            resource.

    An instance of this class will be set to the __json_api_resource__ attribute
    of the class wrapped with the @jsonapi.resource decorator.
    """

    type: str
    id: str
    attributes: dict[str, Any] = field(default_factory=dict)
    relationships: dict[str, Any] = field(default_factory=dict)


def resource(type_: str, id_: str = "id", auto: bool = True):
    """A decorator that defines a class as resource.

    Args:
        type_: The type of the source
        id_: The name of the method or property that is used to get the id of the
            resource. The default is "id".
        auto: When True, which is the default, dataclass and BaseModel classes are
            inspected for attributes and relationships automatically.

    This decorator will instantiate a Resource object and sets the
    __json_api_resource__ attribute of the wrapped class with this object.

    Note:
        The id will always be converted to a string.
    """

    def decorator(cls):
        json_api_resource = Resource(type=type_, id=id_)
        for method_name in dir(cls):
            method = getattr(cls, method_name)
            if hasattr(method, "__json_attribute__"):
                json_api_resource.attributes[method.__json_attribute__] = method
            elif hasattr(method, "__json_relationship__"):
                json_api_resource.relationships[method.__json_relationship__] = method

        cls.__json_api_resource__ = json_api_resource

        if not auto:
            return cls

        def create_getter(attribute_name: str):
            def get(self):
                return getattr(self, attribute_name)

            return get

        # Try to detect attributes/relationships on a dataclass
        if dataclasses.is_dataclass(cls):
            for field_ in dataclasses.fields(cls):
                if field_.name == "id":
                    continue

                if (
                    field_.name in json_api_resource.attributes
                    or field_.name in json_api_resource.relationships
                ):
                    # Skip the field when it was already registered with a decorator.
                    continue

                if hasattr(field_.type, "__json_api_resource__"):
                    json_api_resource.relationships[field_.name] = create_getter(
                        field_.name
                    )
                else:
                    json_api_resource.attributes[field_.name] = create_getter(
                        field_.name
                    )
            return cls

        # Try to detect attributes/relationships on a Pydantic model
        if issubclass(cls, BaseModel):
            for field_ in cls.__fields__.values():
                if field_.name == "id":
                    continue

                if (
                    field_.name in json_api_resource.attributes
                    or field_.name in json_api_resource.relationships
                ):
                    # Skip the field when it was already registered with a decorator.
                    continue

                if hasattr(field_.type_, "__json_api_resource__"):
                    json_api_resource.relationships[field_.name] = create_getter(
                        field_.name
                    )
                else:
                    json_api_resource.attributes[field_.name] = create_getter(
                        field_.name
                    )

        return cls

    return decorator


def attribute(name: str | None = None):
    """A decorator that defines an attribute of a resource.

    Args:
        name: The name of the attribute. When no name is passed, the name of the
            wrapped method will be used.

    The return value of the method that is wrapped with this decorator will be used
    as value of the attribute.
    """

    def decorator(method):
        if name is None:
            method.__json_attribute__ = method.__name__
        else:
            method.__json_attribute__ = name
        return method

    return decorator


def relationship(name: str | None = None):
    """A decorator that defines a relationship of a resource.

    Args:
        name: The name of the relationship. When no name is passed, the name of the
            wrapped method will be used as name.

    The return value of the method that is wrapped with this decorator should be
    a resource. This returned resource will be a relationship of the current resource
    and will be added to the list of included resources.
    """

    def decorator(method):
        if name is None:
            method.__json_relationship__ = method.__name__
        else:
            method.__json_relationship__ = name
        return method

    return decorator


class Document:
    """A class for serializing a resource to a JSON:API object."""

    def __init__(self, data: object | list):
        """Construct a new document class.

        Args:
            data: A resource or a list of resources.

        Note:
            A resource is a class decorated with @jsonapi.resource.
        """
        self._data = data
        self._meta: dict[str, Any] = {}
        self._included: dict[Tuple[str, str], JsonApiData] = {}

    def set_meta(self, *args, **kwargs: dict[str, Any]):
        """Set the meta information.

        Keyword arguments are merged into the meta dictionary.
        When two positional arguments are passed, the first will be used as key, the
        second as value.
        """
        if len(args) == 2:
            self._meta[args[0]] = args[1]
        if kwargs:
            self._meta |= kwargs

    def serialize(self) -> JsonApiDocument:
        """Serialize the data and returns a JSON:API structure.

        Returns:
            A string with the JSON:API structure.
        """
        if isinstance(self._data, list):
            json_data: list[JsonApiData] = []
            for data in self._data:
                json_data.append(self._transform_object(data))
        else:
            json_data: JsonApiData = self._transform_object(self._data)

        if len(self._included):
            return JsonApiDocument(
                meta=self._meta, data=json_data, included=list(self._included.values())
            )
        return JsonApiDocument(meta=self._meta, data=json_data)

    def _transform_object(self, data: object) -> JsonApiData:
        """Transform a resource into a JSON:API data structure."""
        assert hasattr(data, "__json_api_resource__")
        # noinspection PyUnresolvedReferences
        jsonapi_resource: Resource = data.__json_api_resource__

        id_attr = getattr(data, jsonapi_resource.id, None)
        assert id_attr is not None, "No id attribute found in resource"

        if callable(id_attr):
            id_ = str(id_attr())
        else:
            id_ = str(id_attr)

        attributes = {}
        for attr_name, attr_value in jsonapi_resource.attributes.items():
            attributes[attr_name] = attr_value(data)

        json_api_data = JsonApiData(
            type=jsonapi_resource.type, id=id_, attributes=attributes
        )

        relationships = {}
        for rel_name, rel_method in jsonapi_resource.relationships.items():
            linked_resource = self._process_linked_resource(rel_method(data))
            relationships[rel_name] = linked_resource
        if len(relationships) > 0:
            json_api_data.relationships = relationships

        return json_api_data

    def _process_linked_resource(
        self, data: object | list
    ) -> JsonApiRelationship | None:
        """Process a resource or list of resources that is/are a relation of a resource.

        Args:
            data: a linked resource object or a list with linked resource objects.

        Returns:
            A dictionary with a relation type/id or a list with these dictionaries
            when the relation contains multiple resources.
        """
        if data is None:
            return None

        if isinstance(data, list):
            result = []
            for linked_resource in data:
                if linked_resource is not None:
                    relationship_data = self._transform_object(linked_resource)
                    self._include(relationship_data)
                    result.append(
                        JsonApiResourceIdentifier(
                            type=relationship_data.type, id=relationship_data.id
                        )
                    )
            return JsonApiRelationship(data=result)

        relationship_data = self._transform_object(data)
        self._include(relationship_data)
        return JsonApiRelationship(
            data=JsonApiResourceIdentifier(
                type=relationship_data.type,
                id=relationship_data.id,
            )
        )

    def _include(self, data: JsonApiData):
        """Add resource to included.

        To make sure that the included list contains unique values, a tuple with
        the type and id is used as key for the dictionary.
        """
        self._included[(data.type, data.id)] = data
