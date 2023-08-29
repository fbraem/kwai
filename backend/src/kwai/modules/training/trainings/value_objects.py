"""Module that defines a value objects for the bounded context trainings."""

from dataclasses import dataclass

from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.traceable_time import TraceableTime
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
    traceable_time: TraceableTime = TraceableTime()
