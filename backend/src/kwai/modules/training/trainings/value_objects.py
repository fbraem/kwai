"""Module that defines a value object for a season."""

from dataclasses import dataclass

from kwai.core.domain.value_objects.identifier import IntIdentifier


@dataclass(kw_only=True, frozen=True, slots=True)
class Season:
    """A season.

    Attributes:
        id: The id of the season.
        name: The name of the season.
    """

    id: IntIdentifier
    name: str
