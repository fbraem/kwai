"""Module that defines a value object for a season."""

from dataclasses import dataclass

from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.owner import Owner
from kwai.modules.training.coaches.coach import CoachEntity


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
class TrainingCoach:
    """A coach attached to a training."""

    coach: CoachEntity
    owner: Owner
    present: bool = False
    type: int = 0
    payed: bool = False
    remark: str = ""


@dataclass(kw_only=True, frozen=True, slots=True)
class Team:
    """A team.

    Attributes:
        id: The id of the team.
        name: The name of the team.
    """

    id: IntIdentifier
    name: str
