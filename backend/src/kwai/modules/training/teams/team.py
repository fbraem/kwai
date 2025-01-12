"""Module that defines a team entity."""

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.identifier import IntIdentifier

TeamIdentifier = IntIdentifier


class TeamEntity(Entity[TeamIdentifier]):
    """A team.

    Attributes:
        _id: The id of the team.
        _name: The name of the team.
    """

    def __init__(self, *, id_: TeamIdentifier | None = None, name: str):
        super().__init__(id_ or TeamIdentifier())
        self._name = name

    @property
    def name(self) -> str:
        """Return the name of the team."""
        return self._name
