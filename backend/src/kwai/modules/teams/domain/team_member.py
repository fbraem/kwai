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
    """A team member entity.

    A team member entity is an entity which holds specific information of a member
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
    ):
        super().__init__(id_)
        self._name = name
        self._uuid = uuid
        self._license = license
        self._birthdate = birthdate
        self._nationality = nationality
        self._gender = gender

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


@dataclass(kw_only=True, frozen=True, slots=True)
class TeamMember:
    """Represent a member of a team."""

    active: bool
    member: MemberEntity
    traceable_time: TraceableTime
