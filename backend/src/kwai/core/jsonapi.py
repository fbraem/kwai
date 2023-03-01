"""Module that defines some jsonapi related models."""
import json
from dataclasses import dataclass, field
from typing import Any


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


def resource(type_: str, id_: str = "id"):
    """A decorator that defines a class as resource.

    Args:
        type_: The type of the source
        id_: The name of the method or property that is used to get the id of the
            resource. The default is "id".

    This decorator will instantiate a Resource object and sets the
    __json_api_resource__ attribute of the wrapped class with this object.

    Note:
        The id will always be converted to a string.
    """

    def decorator(cls):
        cls.__json_api_resource__ = Resource(type=type_, id=id_)
        for method_name in dir(cls):
            method = getattr(cls, method_name)
            if hasattr(method, "__json_attribute__"):
                cls.__json_api_resource__.attributes[method.__json_attribute__] = method
            elif hasattr(method, "__json_relationship__"):
                cls.__json_api_resource__.relationships[
                    method.__json_relationship__
                ] = method

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
        self._meta = {}
        self._included = {}

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

    def serialize(self) -> str:
        """Serialize the data and returns a JSON:API structure.

        Returns:
            A string with the JSON:API structure.
        """
        json_data: dict[str, Any] = {}
        if len(self._meta) > 0:
            json_data["meta"] = self._meta

        if type(self._data) is list:
            json_data["data"] = []
            for data in self._data:
                json_data["data"].append(self._transform_object(data))
        else:
            json_data["data"] = self._transform_object(self._data)

        if len(self._included):
            json_data["included"] = list(self._included.values())

        return json.dumps(json_data)

    def _transform_object(self, data: object) -> dict[str, Any]:
        """Transform a resource into a JSON:API data structure."""
        assert hasattr(data, "__json_api_resource__")
        # noinspection PyUnresolvedReferences
        jsonapi_resource: Resource = data.__json_api_resource__

        result = {"type": jsonapi_resource.type}
        id_attr = getattr(data, jsonapi_resource.id, None)
        if id_attr:
            if callable(id_attr):
                result["id"] = str(id_attr())
            else:
                result["id"] = str(id_attr)

        attributes = {}
        for attr_name, attr_value in jsonapi_resource.attributes.items():
            attributes[attr_name] = attr_value(data)
        result["attributes"] = attributes

        relationships = {}
        for rel_name, rel_method in jsonapi_resource.relationships.items():
            linked_resource = self._process_linked_resource(rel_method(data))
            if linked_resource is not None:
                relationships[rel_name] = linked_resource
        if len(relationships) > 0:
            result["relationships"] = relationships

        return result

    def _process_linked_resource(
        self, data: object | list
    ) -> dict[str, list[dict[str, str]]] | dict[str, dict[str, str]] | None:
        """Process a resource or list of resources that is/are a relation of a resource.

        Args:
            data: a linked resource object or a list with linked resource objects.

        Returns:
            A dictionary with a relation type/id or a list with these dictionaries
            when the relation contains multiple resources.
        """
        if data is None:
            return

        if type(data) is list:
            result = []
            for linked_resource in data:
                if linked_resource is not None:
                    relationship_data = self._transform_object(linked_resource)
                    self._include(relationship_data)
                    result.append(
                        {
                            "type": relationship_data["type"],
                            "id": relationship_data["id"],
                        }
                    )
            return {"data": result}

        relationship_data = self._transform_object(data)
        self._include(relationship_data)
        return {
            "data": {
                "type": str(relationship_data["type"]),
                "id": str(relationship_data["id"]),
            }
        }

    def _include(self, data: dict[str, Any]):
        """Add resource to included.

        To make sure that the included list contains unique values, a tuple with
        the type and id is used as key for the dictionary.
        """
        self._included[(data["type"], data["id"])] = data
