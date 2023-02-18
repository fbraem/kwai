"""Module that defines a generic entity."""
import inspect
from typing import Generic, TypeVar, Any

from kwai.core.domain.value_objects.identifier import Identifier

T = TypeVar("T", bound=Identifier)


class Entity(Generic[T]):
    """A base class for an entity."""

    def __init__(self, id_: T):
        self._id = id_

    @property
    def id(self) -> T:
        """Return the id of the entity."""
        return self._id

    def has_id(self) -> bool:
        """Has this entity a valid id?

        Returns:
            bool: True when the id is not empty.
        """
        return not self._id.is_empty()

    @classmethod
    def replace(cls, entity: "Entity[T]", **changes) -> Any:
        """Return a new entity from the existing entity.

        Args:
            entity(Entity[T]: The entity to copy the values from
            changes: the values to override when creating the new entity.

        Use the same keyword arguments as used on the class constructor (__init__) to
        replace the existing value of an attribute.
        The class constructor will be called to create this new entity.
        The arguments of the constructor that are not passed in "changes", will get
        the value from the current entity.

        Note:
            To make it clear that the attributes of an entity are private, they are
            prefixed with a underscore. The name of the keyword argument does not
            contain this underscore. This method will try to find the attribute first
            without underscore. When no attribute exists with that name, it will try
            to find it with an underscore.
            When an argument of the constructor contains an underscore as suffix (to
            avoid naming conflicts for example), the underscore will be removed to find
            the attribute of the class.
        """
        ctor_arguments = inspect.signature(entity.__class__.__init__).parameters
        for argument in ctor_arguments:
            # self is not needed
            if argument == "self":
                continue

            # We already have the value when the argument is passed
            if argument in changes:
                continue

            # The attribute is not passed, so we need to use the original value.

            # Try to get the value of a public attribute
            attribute_name = argument.removesuffix("_")
            if attribute_name in entity.__dict__:
                changes[argument] = entity.__dict__[attribute_name]
                continue

            # Try to get the value of the private attribute
            private_attribute_name = "_" + attribute_name
            if private_attribute_name in entity.__dict__:
                changes[argument] = entity.__dict__[private_attribute_name]
                continue

        return entity.__class__(**changes)
