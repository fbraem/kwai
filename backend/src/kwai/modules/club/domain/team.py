"""Module for defining the team entity."""

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.traceable_time import TraceableTime

TeamIdentifier = IntIdentifier


class TeamEntity(Entity[TeamIdentifier]):
    """Entity for a team of the club."""

    def __init__(
        self,
        *,
        id_: TeamIdentifier | None = None,
        name: str,
        active: bool = True,
        remark: str = "",
        traceable_time: TraceableTime | None = None,
    ):
        super().__init__(id_ or TeamIdentifier())
        self._name = name
        self._active = active
        self._remark = remark
        self._traceable_time = traceable_time or TraceableTime()

    @property
    def name(self) -> str:
        """Return the name of the team."""
        return self._name

    @property
    def is_active(self):
        """Is this team active?"""
        return self._active

    @property
    def remark(self) -> str:
        """Return the remark of the team."""
        return self._remark

    @property
    def traceable_time(self) -> TraceableTime:
        """Return the traceable_time."""
        return self._traceable_time
