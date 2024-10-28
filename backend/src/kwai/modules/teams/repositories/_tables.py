from dataclasses import dataclass
from datetime import date, datetime
from typing import Self

from kwai.core.db.table_row import TableRow
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.club.domain.country import CountryEntity, CountryIdentifier
from kwai.modules.teams.domain.team import TeamEntity, TeamIdentifier
from kwai.modules.teams.domain.team_member import MemberEntity, TeamMember


@dataclass(kw_only=True, frozen=True, slots=True)
class TeamRow(TableRow):
    """Represents a row of the teams table."""

    __table_name__ = "teams"

    id: int
    name: str
    season_id: int | None
    team_category_id: int | None
    active: int
    remark: str | None
    created_at: datetime
    updated_at: datetime | None

    def create_entity(self, team_members: dict[UniqueId, TeamMember]) -> TeamEntity:
        return TeamEntity(
            id_=TeamIdentifier(self.id),
            name=self.name,
            active=self.active == 1,
            remark=self.remark or "",
            members=team_members,
        )

    @classmethod
    def persist(cls, team: TeamEntity) -> Self:
        return cls(
            id=team.id.value,
            name=team.name,
            season_id=None,
            team_category_id=None,
            active=1 if team.is_active else 0,
            remark=team.remark,
            created_at=team.traceable_time.created_at.timestamp,  # type: ignore[arg-type]
            updated_at=team.traceable_time.updated_at.timestamp,
        )


@dataclass(kw_only=True, frozen=True, slots=True)
class MemberRow(TableRow):
    """Represents a row of the members table used for a team member."""

    __table_name__ = "judo_members"

    id: int | None
    uuid: str | None
    license: str | None
    license_end_date: date | None
    person_id: int | None
    active: int | None


@dataclass(kw_only=True, frozen=True, slots=True)
class MemberPersonRow(TableRow):
    """Represents a row of the persons table used for a team member."""

    __table_name__ = "persons"

    id: int | None
    firstname: str | None
    lastname: str | None
    gender: int | None
    birthdate: date | None
    nationality_id: int | None


@dataclass(kw_only=True, frozen=True, slots=True)
class TeamMemberRow(TableRow):
    """Represents a row of the team members table."""

    __table_name__ = "team_members"

    team_id: int | None
    member_id: int | None
    active: int | None
    created_at: datetime | None
    updated_at: datetime | None

    def create_team_member(self, member: MemberEntity):
        return TeamMember(
            active=True if self.active == 1 else False,
            member=member,
            traceable_time=TraceableTime(
                created_at=Timestamp(self.created_at),
                updated_at=Timestamp(self.updated_at),
            ),
        )

    @classmethod
    def persist(cls, team: TeamEntity, team_member: TeamMember) -> Self:
        """Persist a team member to the table row."""
        return cls(
            team_id=team.id.value,
            member_id=team_member.member.id.value,
            active=1 if team_member.active else 0,
            created_at=team_member.traceable_time.created_at.timestamp,  # type: ignore[arg-type]
            updated_at=team_member.traceable_time.updated_at.timestamp,
        )


@dataclass(kw_only=True, frozen=True, slots=True)
class CountryRow(TableRow):
    """Represent a row of the countries table.

    Attributes:
        id: The id of the country.
        iso_2: The ISO 2 code of the country.
        iso_3: The ISO 3 code of the country.
    """

    __table_name__ = "countries"

    id: int | None = None
    iso_2: str | None
    iso_3: str | None
    name: str | None
    created_at: datetime | None
    updated_at: datetime | None

    def create_country(self) -> CountryEntity:
        """Create a Country value object from the row.

        Returns:
            A country value object.
        """
        return CountryEntity(
            id_=CountryIdentifier(self.id),
            iso_2=self.iso_2,
            iso_3=self.iso_3,
            name=self.name,
        )
