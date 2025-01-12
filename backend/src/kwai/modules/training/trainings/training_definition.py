"""Module for defining a training definition entity."""

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.time_period import TimePeriod
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.weekday import Weekday
from kwai.modules.training.teams.team import TeamEntity

TrainingDefinitionIdentifier = IntIdentifier


class TrainingDefinitionEntity(Entity[TrainingDefinitionIdentifier]):
    """A training definition entity.

    A training definition can be used to create recurring trainings.
    """

    def __init__(
        self,
        *,
        id_: TrainingDefinitionIdentifier | None = None,
        name: str,
        description: str,
        weekday: Weekday,
        period: TimePeriod,
        active: bool = True,
        location: str = "",
        remark: str = "",
        team: TeamEntity | None = None,
        owner: Owner,
        traceable_time: TraceableTime | None = None,
    ):
        """Initialize a training definition.

        Args:
            id_: The id of the training definition.
            name: The name of the training definition.
            description: A description of the training definition.
            weekday: The weekday to use to create the recurring trainings.
            period: The time period to use to create the recurring trainings.
            active: Is this definition active?
            location: The location of the recurring trainings.
            remark: A remark about this training definition.
            team: A team that is associated with the definition.
            owner: The owner of this training definition.
            traceable_time: The creation and modification timestamp of the definition.
        """
        super().__init__(id_ or TrainingDefinitionIdentifier())
        self._name = name
        self._description = description
        self._weekday = weekday
        self._period = period
        self._active = active
        self._location = location
        self._remark = remark
        self._team = team
        self._owner = owner
        self._traceable_time = traceable_time or TraceableTime()

    @property
    def id(self) -> TrainingDefinitionIdentifier:
        """Return the id of the training definition."""
        return self._id

    @property
    def name(self) -> str:
        """Return the name of the training definition."""
        return self._name

    @property
    def description(self) -> str:
        """Return the description of the training definition."""
        return self._description

    @property
    def weekday(self) -> Weekday:
        """Return the weekday of the training definition."""
        return self._weekday

    @property
    def period(self) -> TimePeriod:
        """Return the period of the training definition."""
        return self._period

    @property
    def active(self) -> bool:
        """Return True when the training definition is active."""
        return self._active

    @property
    def location(self) -> str:
        """Return the location of the training definition."""
        return self._location

    @property
    def owner(self) -> Owner:
        """Return the owner of the training definition."""
        return self._owner

    @property
    def remark(self) -> str:
        """Return the remark of the training definition."""
        return self._remark

    @property
    def traceable_time(self) -> TraceableTime:
        """Return the creation/modification timestamp of this training definition."""
        return self._traceable_time

    @property
    def team(self) -> TeamEntity:
        """Return the team that is associated with this definition."""
        return self._team
