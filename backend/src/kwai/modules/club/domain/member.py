"""Module for defining the Member entity."""

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.club.domain.person import PersonEntity
from kwai.modules.club.members.value_objects import License

MemberIdentifier = IntIdentifier


class MemberEntity(Entity[MemberIdentifier]):
    """A member entity."""

    def __init__(
        self,
        *,
        id_: MemberIdentifier | None = None,
        uuid: UniqueId | None = None,
        license: License,
        person: PersonEntity,
        remark: str = "",
        active: bool = True,
        competition: bool = False,
        traceable_time: TraceableTime | None = None,
    ):
        """Initialize a member.

        Args:
            id_: The id of the member.
            uuid: A unique id for the member.
            license: The license of the member.
            person: The related person entity.
            remark: A remark about the member.
            active: Is this member still member of the club?
            competition: Is this member participating in competitions?
            traceable_time: The creation and modification timestamp of the training.
        """
        super().__init__(id_ or MemberIdentifier())
        self._uuid = uuid or UniqueId.generate()
        self._license = license
        self._person = person
        self._remark = remark
        self._active = active
        self._competition = competition
        self._traceable_time = traceable_time or TraceableTime()

    @property
    def is_active(self) -> bool:
        """Is this member active?"""
        return self._active

    @property
    def is_competitive(self) -> bool:
        """Is this member participating in competition?"""
        return self._competition

    @property
    def license(self) -> License:
        """Return the license."""
        return self._license

    @property
    def person(self) -> PersonEntity:
        """Return the person."""
        return self._person

    @property
    def traceable_time(self) -> TraceableTime:
        """Return the traceable_time."""
        return self._traceable_time

    @property
    def remark(self) -> str:
        """Return the remark."""
        return self._remark

    @property
    def uuid(self) -> UniqueId:
        """Return the uuid."""
        return self._uuid
