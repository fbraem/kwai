"""Module for defining the team member entity."""

from dataclasses import dataclass

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.club.domain.country import CountryEntity
from kwai.modules.club.domain.value_objects import Birthdate, Gender, License


MemberIdentifier = IntIdentifier


class MemberEntity(Entity[MemberIdentifier]):
    """A member entity.

    A member entity is an entity which holds specific information of a member
    that can be used for a member of a team.
    """

    def __init__(
        self,
        *,
        id_: MemberIdentifier,
        uuid: UniqueId,
        name: Name,
        license: License,
        birthdate: Birthdate,
        nationality: CountryEntity,
        gender: Gender,
        active_in_club: bool = True,
    ):
        super().__init__(id_)
        self._name = name
        self._uuid = uuid
        self._license = license
        self._birthdate = birthdate
        self._nationality = nationality
        self._gender = gender
        self._active_in_club = active_in_club

    def __str__(self) -> str:
        """Return a string of this entity."""
        return f"{self._uuid} - {self._name}"

    def __repr__(self) -> str:
        """Return a representation of this entity."""
        return f"<{self.__class__.__name__} id={self.id}, uuid={self.uuid}, name={self.name}>"

    @property
    def name(self) -> Name:
        """Return the name."""
        return self._name

    @property
    def uuid(self) -> UniqueId:
        """Return the uuid."""
        return self._uuid

    @property
    def license(self) -> License:
        """Return the license."""
        return self._license

    @property
    def birthdate(self) -> Birthdate:
        """Return the birthdate."""
        return self._birthdate

    @property
    def nationality(self) -> CountryEntity:
        """Return the nat."""
        return self._nationality

    @property
    def gender(self) -> Gender:
        """Return the gender."""
        return self._gender

    @property
    def is_active_in_club(self) -> bool:
        """Return if the member is active."""
        return self._active_in_club


@dataclass(kw_only=True, frozen=True, slots=True)
class TeamMember:
    """Represent a member of a team.

    When active is False, it means the member is not active for the team it belongs
    to.
    """

    active: bool = False
    member: MemberEntity
    traceable_time: TraceableTime = TraceableTime()
