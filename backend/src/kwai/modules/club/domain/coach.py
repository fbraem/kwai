"""Module for defining a coach entity."""

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.modules.club.domain.member import MemberEntity

CoachIdentifier = IntIdentifier


class CoachEntity(Entity[CoachIdentifier]):
    """A coach entity."""

    def __init__(
        self,
        *,
        id_: CoachIdentifier | None = None,
        member: MemberEntity,
        description: str = "",
        diploma: str = "",
        active: bool = True,
        remark: str = "",
        user: Owner | None = None,
        traceable_time: TraceableTime | None = None,
    ):
        """Initialize a coach.

        Args:
            id_ (CoachIdentifier): The id of the coach.
            member: A coach is a member of the club.
            description: The description (bio) of the coach.
            diploma: The diploma of the coach.
            active: Whether the coach is active.
            remark: A remark about the coach.
            user: A coach can also be a user of the system.
            traceable_time: The creation and modification timestamp of the coach.
        """
        super().__init__(id_ or CoachIdentifier())
        self._member = member
        self._description = description
        self._diploma = diploma
        self._active = active
        self._remark = remark
        self._user = user
        self._traceable_time = traceable_time or TraceableTime()

    @property
    def is_active(self) -> bool:
        """Is the coach active?"""
        return self._active

    @property
    def member(self) -> MemberEntity:
        """Return the related member."""
        return self._member

    @property
    def name(self) -> Name:
        """Return the name of the coach."""
        return self._member.person.name

    @property
    def diploma(self) -> str:
        """Return the diploma of the coach."""
        return self._diploma

    @property
    def description(self) -> str:
        """Return the description of the coach."""
        return self._description

    @property
    def remark(self) -> str:
        """Return the remark of the coach."""
        return self._remark

    @property
    def traceable_time(self) -> TraceableTime:
        """Return the traceable_time."""
        return self._traceable_time

    @property
    def uuid(self):
        """Return the uuid of the coach."""
        return self._member.uuid

    @property
    def user(self) -> Owner | None:
        """Return the related user."""
        return self._user
