"""Module that defines a value object for a season."""

from dataclasses import dataclass

from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.name import Name


@dataclass(kw_only=True, frozen=True, slots=True)
class Season:
    """A season.

    Attributes:
        id: The id of the season.
        name: The name of the season.
    """

    id: IntIdentifier
    name: str


@dataclass(kw_only=True, frozen=True, slots=True)
class Coach:
    """A coach of a training.

    Attributes:
        id: The id of the coach.
        name: The name of the coach.
    """

    id: IntIdentifier
    name: Name


@dataclass(kw_only=True, frozen=True, slots=True)
class Team:
    """A team.

    Attributes:
        id: The id of the team.
        name: The name of the team.
    """

    id: IntIdentifier
    name: str
