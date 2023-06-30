"""Module that defines some jsonapi related models."""
import dataclasses
from types import NoneType
from typing import Any, Callable, Optional, Type, Union, get_args, get_origin

from fastapi import Query
from pydantic import BaseModel, Extra, Field, create_model


class Meta(BaseModel):
    """Defines the metadata for the document model.

    Attributes:
        count: The number of actual resources
        offset: The offset of the returned resources (pagination)
        limit: The maximum number of returned resources (pagination)

    A limit of 0, means there was no limit was set.
    """

    count: int | None = None
    offset: int | None = None
    limit: int | None = None

    class Config:
        """Allow extra attributes on the Meta object."""

        extra = Extra.allow


class DocumentBaseModel(BaseModel):
    """A basemodel for a document."""

    meta: Meta | None = None

    def dict(self, *args, **kwargs) -> dict[str, Any]:
        """Overloads dict to remove 'meta' when it's None."""
        if self.meta is None:
            exclude = kwargs.get("exclude", None)
            if exclude is None:
                kwargs["exclude"] = {"meta"}
            else:
                kwargs["exclude"].add("meta")
        return super().dict(*args, **kwargs)


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class Attribute:
    """Dataclass for storing information about attributes."""

    name: str
    getter: Callable
    type: Type
    optional: bool = dataclasses.field(init=False)

    def __post_init__(self):
        """Set the optional field."""
        all_types = get_args(self.type)
        object.__setattr__(self, "optional", NoneType in all_types)


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class Relationship:
    """Dataclass for storing information about relationships."""

    name: str
    getter: Callable
    type: Type
    optional: bool = dataclasses.field(init=False)
    iterable: bool = dataclasses.field(init=False)
    resource_type: Type = dataclasses.field(init=False)

    def __post_init__(self):
        """Initialise the properties that depend on the type."""
        all_types = get_args(self.type)
        object.__setattr__(self, "optional", NoneType in all_types)

        if self.optional:
            non_optional_type = all_types[all_types.index(NoneType) ^ 1]
        else:
            non_optional_type = self.type

        origin = get_origin(non_optional_type)
        object.__setattr__(self, "iterable", origin is list)

        if self.iterable:
            object.__setattr__(self, "resource_type", get_args(non_optional_type)[0])
        else:
            object.__setattr__(self, "resource_type", non_optional_type)


class Resource:
    """A class that is responsible for generating all the models needed for JSON:API.

    Use the resource decorator to mark a class as a JSON:API resource. The decorator
    will attach an instance of this class to the marked class.
    """

    def __init__(self, resource):
        self._resource = resource
        self._type = ""
        self._id_getter = None
        self._attributes = {}
        self._relationships = {}

        self._resource_identifier_model = None
        self._attributes_model = None
        self._relationships_model = None
        self._resource_model = None
        self._document_model = None

    def get_attribute(self, attribute_name: str) -> Attribute | None:
        """Return the attribute definition for the given name.

        None is returned, when the attribute does not exist.
        """
        return self._attributes.get(attribute_name, None)

    def get_resource_attribute(self, attribute_name: str, resource_instance):
        """Return the value of the attribute from the resource.

        The getter created when scanning the class for the attributes will
        be used to retrieve the attribute value from the resource.
        """
        attr = self.get_attribute(attribute_name)

        if attr is None:
            return
        return attr.getter(resource_instance)

    def get_resource_attributes(self, resource_instance) -> dict[str, Any]:
        """Get all attribute values from the resource instance."""
        values = {}
        for attr in self._attributes.values():
            values[attr.name] = attr.getter(resource_instance)
        return values

    def get_relationship(self, relationship_name: str) -> Relationship | None:
        """Return the relationship definition for the given name.

        None is returned, when the relationship does not exist.
        """
        return self._relationships.get(relationship_name, None)

    def get_resource_relationships(self, resource_instance) -> dict[str, Any]:
        """Get all relationship values from the resource instance."""
        values = {}
        for rel in self._relationships.values():
            values[rel.name] = rel.getter(resource_instance)
        return values

    def get_type(self) -> str:
        """Get the resource type."""
        return self._type

    def get_resource_object(self, resource_instance) -> tuple:
        """Get the resource from the resource instance.

        It returns a tuple. The first value will contain the resource object, while
        the second value will contain a list of the related resource objects.
        """
        attributes = self.get_resource_attributes(resource_instance)
        related_resource_objects = set()

        relationships = {}
        for rel in self._relationships.values():
            rel_value = rel.getter(resource_instance)

            relationship_model = self._relationships_model.__fields__[rel.name].type_

            if rel_value is None:
                relationship_value = None
            elif rel.iterable:
                relationship_value = []
                for value in rel_value:
                    relationship_value.append(
                        value.__json_api_resource__.get_resource_identifier(value)
                    )
                    # Get all related resources.
                    related_resource = value.__json_api_resource__.get_resource_object(
                        value
                    )
                    related_resource_objects.add(related_resource[0])
                    for r in related_resource[1]:
                        related_resource_objects.add(r)
            else:
                relationship_value = (
                    rel_value.__json_api_resource__.get_resource_identifier(rel_value)
                )
                # Get all related resources.
                related_resource = rel_value.__json_api_resource__.get_resource_object(
                    rel_value
                )
                related_resource_objects.add(related_resource[0])
                for r in related_resource[1]:
                    related_resource_objects.add(r)

            relationships[rel.name] = relationship_model(data=relationship_value)

        resource_model = self.get_resource_model()
        return (
            resource_model(
                id=self.get_resource_id(resource_instance),
                attributes=attributes,
                relationships=relationships,
            ),
            related_resource_objects,
        )

    def has_id(self) -> bool:
        """Check if there is an id available in the resource."""
        return self._id_getter is not None

    def get_resource_id(self, resource_instance):
        """Return the id of the resource.

        The getter created when scanning the class for the id property/method will
        be used to retrieve the id from the resource.
        """
        return self._id_getter(resource_instance)

    def build(self, auto: bool = True) -> "Resource":
        """Build the JSONAPI resource models."""
        self._type = getattr(self._resource, "__json_api_resource_type__", "")

        assert len(self._type) > 0, (
            "Is this a JSON_API resource? Did you forget the "
            "json_api.resource decorator?"
        )

        self._scan_class_attributes()
        if auto:
            if dataclasses.is_dataclass(self._resource):
                self._scan_dataclass()
            elif issubclass(self._resource, BaseModel):
                self._scan_base_model()

        self._create_resource_identifier_model()
        self._create_resource_model()
        self._create_document_model()

        assert self._id_getter is not None, (
            "Can't determine the id of the resource. "
            "Use the id decorator or define an 'id' field."
        )

        return self

    def _scan_class_attributes(self):
        """Search for attributes, id and relationships in the class.

        This method will check the attributes of a class if they are decorated with
        attribute, id or relationship decorators.
        """
        for attribute_name in dir(self._resource):
            class_attribute = getattr(self._resource, attribute_name)
            if not callable(class_attribute):
                continue

            # First check if the jsonapi.attribute decorator was used to define an
            # attribute.
            json_api_attribute_name = getattr(
                class_attribute, "__json_api_attribute__", None
            )
            if json_api_attribute_name is not None:
                self._attributes[json_api_attribute_name] = Attribute(
                    name=json_api_attribute_name,
                    getter=class_attribute,
                    type=class_attribute.__annotations__["return"],
                )
                continue

            # Check if json_api.id decorator is used to define a method to get the id
            # of a resource.
            if hasattr(class_attribute, "__json_api_id__"):
                self._id_getter = class_attribute
                continue

            # Check if jsonapi.relationship is used to define relationships
            json_api_relationship_name = getattr(
                class_attribute, "__json_api_relationship__", None
            )
            if json_api_relationship_name is not None:
                self._relationships[json_api_relationship_name] = Relationship(
                    name=json_api_relationship_name,
                    getter=class_attribute,
                    type=class_attribute.__annotations__["return"],
                )

    @classmethod
    def _create_getter(cls, attribute_name: str):
        """Create a method for getting the value of an attribute."""

        def get(self):
            return getattr(self, attribute_name)

        return get

    def _scan_dataclass(self):
        """Search for attributes, id and relationships in a dataclass.

        A field with a __json_api_resource__ attribute is a relationship. A field with
        the name "id" will be used as id of the resource. All other fields are
        attributes. When a field has a name that is already used with an
        attribute, id or relationship decorator, it will be skipped.
        """
        for field_ in dataclasses.fields(self._resource):
            # When the field name is 'id' and there is not a method decorated with
            # jsonapi.id, then this will be the id of the resource.
            if field_.name == "id":
                if self._id_getter is None:
                    self._id_getter = self._create_getter("id")
                continue

            # Skip the field when it was already registered with a decorator.
            if field_.name in self._attributes or field_.name in self._relationships:
                continue

            # When the field has a type that was decorated with json_api.resource,
            # then the field is a relationship.
            if hasattr(field_.type, "__json_api_resource__"):
                self._relationships[field_.name] = Relationship(
                    name=field_.name,
                    getter=self._create_getter(field_.name),
                    type=field_.type,
                )
                continue

            # This is an attribute.
            self._attributes[field_.name] = Attribute(
                name=field_.name,
                getter=self._create_getter(field_.name),
                type=field_.type,
            )

    def _scan_base_model(self):
        """Search for attributes and relationships on a BaseModel class.

        A field with a __json_api_resource__ attribute is a relationship. A field with
        the name "id" will be used as id of the resource. All other fields are
        attributes. When a field has a name that is already used with an
        attribute, id or relationship decorator, it will be skipped.
        """
        for field_ in self._resource.__fields__.values():
            # When the field name is 'id' and there is not a method decorated with
            # jsonapi.id, then this will be the id of the resource.
            if field_.name == "id":
                if self._id_getter is None:
                    self._id_getter = self._create_getter("id")
                continue

            # Skip the field when it was already registered with a decorator.
            if field_.name in self._attributes or field_.name in self._relationships:
                continue

            # When the field has a type that was decorated with json_api.resource,
            # then the field is a relationship.
            if hasattr(field_.type_, "__json_api_resource__"):
                self._relationships[field_.name] = Relationship(
                    name=field_.name,
                    getter=self._create_getter(field_.name),
                    type=field_.annotation,
                )
                continue

            # This is an attribute.
            self._attributes[field_.name] = Attribute(
                name=field_.name,
                getter=self._create_getter(field_.name),
                type=field_.type_,
            )

    def __str__(self) -> str:
        """Use type as string representation."""
        return f"type: {self._type}"

    def _create_resource_identifier_model(self) -> None:
        """Create a resource identifier model, if it wasn't created yet."""
        if self._resource_identifier_model is not None:
            return

        def hash_resource(resource_instance):
            """Create a hash for a resource."""
            return hash(resource_instance.type + "." + resource_instance.id)

        self._resource_identifier_model = create_model(
            self.get_model_class_prefix() + "ResourceIdentifier",
            **{
                "id": (str | None, Field(default=None)),
                "type": (str, Field(const=True, default=self._type)),
            },
        )
        self._resource_identifier_model.__hash__ = hash_resource

    def get_resource_identifier_model(self):
        """Return the resource identifier model.

        The resource identifier model contains the id and type of the resource.
        """
        return self._resource_identifier_model

    def get_resource_identifier(self, resource_instance):
        """Get an instance of the resource identifier.

        A resource identifier contains the id and the type of the resource.
        """
        return self._resource_identifier_model(
            id=self.get_resource_id(resource_instance)
        )

    def get_model_class_prefix(self) -> str:
        """Return the prefix used for creating the model classes.

        The prefix is the name of the class without the "Resource" suffix.
        """
        return self._resource.__name__.removesuffix("Resource") + "_"

    def _create_resource_model(self):
        """Create the resource model."""
        if self._resource_model is not None:
            return

        # Create a model for the attributes of the resource.
        attributes = {}
        for attr in self._attributes.values():
            if attr.optional:
                attributes[attr.name] = (attr.type, Field(default=None))
            else:
                attributes[attr.name] = (attr.type, ...)

        self._attributes_model = create_model(
            self.get_model_class_prefix() + "Attributes", **attributes
        )

        resource_model_fields = {"attributes": (self._attributes_model, ...)}

        if len(self._relationships) > 0:
            # Create a model for the relationships of the resource.
            relationships = {}
            for rel in self._relationships.values():
                if hasattr(rel.resource_type, "__json_api_resource__"):
                    rel_type = (
                        rel.resource_type.__json_api_resource__.get_resource_identifier_model()
                    )

                    if rel.iterable:
                        rel_type = list[rel_type]
                    if rel.optional:
                        rel_type |= None

                    relationship_object_model = create_model(
                        self.get_model_class_prefix()
                        + rel.name.capitalize()
                        + "Relationship",
                        data=(rel_type, ...),
                    )

                    relationships[rel.name] = (
                        Optional[relationship_object_model],
                        None if rel.optional else ...,
                    )

            self._relationships_model = create_model(
                self.get_model_class_prefix() + "Relationships", **relationships
            )
            resource_model_fields["relationships"] = (
                self._relationships_model,
                ...,
            )

        self._resource_model = create_model(
            self.get_model_class_prefix() + "Resource",
            __base__=self.get_resource_identifier_model(),
            **resource_model_fields,
        )

    def get_resource_model(self):
        """Get the resource model.

        The resource model contains the id, type, attributes and relationships of the
        resource.
        """
        return self._resource_model

    def _create_document_model(self):
        """Create the document model.

        The document model is the main model of the resource.
        """
        if self._document_model is not None:
            return

        resource_model = self.get_resource_model()

        document_fields = {
            "data": (
                resource_model | list[resource_model],
                Field(default_factory=list),
            ),
        }
        if len(self._relationships) > 0:
            # included is a list with all related resource types.
            relation_types = ()
            for rel in self._relationships.values():
                relation_types = relation_types + (
                    rel.resource_type.__json_api_resource__.get_resource_model(),
                )
                document_fields["included"] = (
                    list[Union[relation_types]],  # type: ignore
                    Field(default_factory=list),
                )

        self._document_model = create_model(
            self.get_model_class_prefix() + "Document",
            __base__=DocumentBaseModel,
            **document_fields,
        )

    def get_document_model(self):
        """Get the document model."""
        return self._document_model

    def serialize(self, resource_instance):
        """Serialize the resource instance into a document model."""
        resource_object, related_objects = self.get_resource_object(resource_instance)
        included = set(related_objects)
        document_model = self.get_document_model()

        return document_model(data=resource_object, included=list(included))

    def serialize_list(self, resource_instances: list[Any]):
        """Serialize a list of resources into a document model."""
        included = set()
        resources = []
        for resource_instance in resource_instances:
            resource_object, related_objects = self.get_resource_object(
                resource_instance
            )
            resources.append(resource_object)
            included = included | related_objects

        document_model = self.get_document_model()
        return document_model(data=resources, included=list(included))


def resource(type_: str, auto: bool = True):
    """Turn a class into a JSONAPI resource with this decorator."""

    def decorator(cls):
        cls.__json_api_resource_type__ = type_

        json_api_resource = Resource(cls).build(auto)
        cls.__json_api_resource__ = json_api_resource
        cls.serialize = lambda resource_instance: json_api_resource.serialize(
            resource_instance
        )
        cls.serialize_list = lambda resource_list: json_api_resource.serialize_list(
            resource_list
        )
        cls.get_document_model = lambda: json_api_resource.get_document_model()

        return cls

    return decorator


def attribute(_func=None, *, name: str | None = None):
    """Turn a method into an attribute of a resource with this decorator.

    When name is omitted, the name of the method is used. Brackets can be omitted when
    no name is passed.
    """

    def inner_function(fn):
        fn.__json_api_attribute__ = name or fn.__name__
        return fn

    if _func is None:
        return inner_function

    return inner_function(_func)


def relationship(_func=None, *, name: str | None = None):
    """Turn a method into a relationship of a resource with this decorator.

    When name is omitted, the name of the method is used. Brackets can be omitted when
    no name is passed.
    """

    def inner_function(fn):
        fn.__json_api_relationship__ = name or fn.__name__
        return fn

    if _func is None:
        return inner_function

    return inner_function(_func)


def id(_func=None):
    """Mark this method as the way to get the id of the resource with this decorator.

    Brackets can be omitted.
    """

    def inner_function(fn):
        fn.__json_api_id__ = True
        return fn

    if _func is None:
        return inner_function

    return inner_function(_func)


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
