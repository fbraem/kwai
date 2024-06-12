from dataclasses import dataclass
from datetime import date, datetime
from typing import Self

from kwai.core.db.table_row import TableRow
from kwai.modules.teams.domain.team import TeamEntity


@dataclass(kw_only=True, frozen=True, slots=True)
class TeamRow(TableRow):
    """Represents a row of the teams table."""

    __table_name__ = "teams"

    id: int
    name: str
    season_id: int | None
    team_category_id: int | None
    active: int
    remark: str
    created_at: datetime
    updated_at: datetime | None

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
class TeamMemberRow(TableRow):
    """Represents a row of the members table used for a team member."""

    __table_name__ = "judo_members"

    id: int
    uuid: str
    license: str
    license_end_date: date
    person_id: int


@dataclass(kw_only=True, frozen=True, slots=True)
class TeamMemberPersonRow(TableRow):
    """Represents a row of the persons table used for a team member."""

    __table_name__ = "persons"

    id: int
    firstname: str
    lastname: str
    gender: int
    birthdate: date
    nationality_id: int


@dataclass(kw_only=True, frozen=True, slots=True)
class TeamMembersRow(TableRow):
    """Represents a row of the team members table."""

    __table_name__ = "team_members"

    team_id: int
    member_id: int
    active: int
    created_at: datetime
    updated_at: datetime | None
