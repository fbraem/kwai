"""Module that defines a value object for an owner of an entity."""

from dataclasses import dataclass

from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.unique_id import UniqueId


@dataclass(kw_only=True, frozen=True, slots=True)
class Owner:
    """A value object for an owner of an entity.

    Attributes:
        id: The id of the owner (user)
        uuid: The unique id of the owner (user)
        name: The name of the owner
    """

    id: IntIdentifier
    uuid: UniqueId
    name: Name
