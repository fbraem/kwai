"""Module that defines a generic entity."""

import inspect

from dataclasses import dataclass, field, fields, replace
from typing import (
    Any,
    ClassVar,
    Self,
)

from kwai.core.domain.value_objects.identifier import Identifier, IntIdentifier
from kwai.core.domain.value_objects.traceable_time import TraceableTime


@dataclass(frozen=True, slots=True, eq=False)
class DataclassEntity:
    """A base class for an entity.

    An entity is immutable, so it cannot be modified. A method of an entity that
    changes the entity must allways return a new entity instance with the changed
    data. The method replace of dataclasses can be used for this.

    Currently, this is a separate class to make it possible to migrate to this
    new class. In the future, the Entity class will be removed and this class
    will be renamed to Entity.

    By default, id is of type IntIdentifier. Overwrite ID in an entity class if
    another identifier should be used.

    Attributes:
        id: The id of the entity.
        traceable_time: Keeps track of the creation and update timestamp of the entity.
    """

    ID: ClassVar = IntIdentifier

    id: ID = None
    traceable_time: TraceableTime = field(default_factory=TraceableTime)
    version = 0

    def __post_init__(self):
        """When is id is not set, a default id is created."""
        if self.id is None:
            object.__setattr__(self, "id", self.ID())

    def set_id(self, id_: ID) -> Self:
        """Set the id for this entity.

        This will raise a ValueError if the id was already set.
        If you need an entity with the same data but with another id, you should create
        a new entity with dataclasses.replace and replace the id.
        """
        if not self.id.is_empty():
            raise ValueError(f"{self.__class__.__name__} has already an ID: {self.id}")
        return replace(self, id=id_)

    def shallow_dict(self) -> dict[str, Any]:
        """Return a dictionary representation of the entity.

        !!! Note
            This method is not recursive. Use asdict from dataclasses when also
            nested fields must be returned as a dict.
        """
        return {f.name: getattr(self, f.name) for f in fields(self)}

    def __eq__(self, other: Any) -> bool:
        """Check if two entities are equal.

        An entity equals another entity when the id is the same.
        """
        return isinstance(other, type(self)) and other.id == self.id

    def __hash__(self) -> int:
        """Generate a hash for this entity."""
        return hash(self.id)


class Entity[T: Identifier]:
    """A base class for an entity."""

    def __init__(self, id_: T):
        self._id = id_

    @property
    def id(self) -> T:
        """Return the id of the entity."""
        return self._id

    def has_id(self) -> bool:
        """Check if this entity has a valid id.

        Returns:
            bool: True when the id is not empty.
        """
        return not self._id.is_empty()

    @classmethod
    def replace(cls, entity: Self, **changes: Any) -> Any:
        """Return a new entity from the existing entity.

        Args:
            entity: The entity to copy the values from
            changes: the values to override when creating the new entity.

        Use the same keyword arguments as used on the class constructor (__init__) to
        replace the existing value of an attribute.
        The class constructor will be called to create this new entity.
        The arguments of the constructor that are not passed in "changes", will get
        the value from the current entity.

        Note:
            To make it clear that the attributes of an entity are private, they are
            prefixed with an underscore. The name of the keyword argument does not
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
