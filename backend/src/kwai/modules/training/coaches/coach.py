"""Module that defines a coach entity."""
from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.name import Name

CoachIdentifier = IntIdentifier


class CoachEntity(Entity[CoachIdentifier]):
    """A coach.

    Attributes:
        _id: The id of the coach.
        _name: The name of the coach.
    """

    def __init__(self, *, id_: CoachIdentifier | None = None, name: Name, active: bool):
        super().__init__(id_ or CoachIdentifier())
        self._id = id_
        self._name = name
        self._active = active

    @property
    def name(self) -> Name:
        """Return the name of the coach."""
        return self._name

    @property
    def is_active(self) -> bool:
        """Return True when the coach is still active, False otherwise."""
        return self._active
