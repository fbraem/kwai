"""Module that defines a database query for team members."""

from collections import defaultdict
from dataclasses import dataclass
from typing import Self

from sql_smith.functions import on

from kwai.core.db.database_query import DatabaseQuery
from kwai.core.db.table_row import JoinedTableRow
from kwai.core.domain.value_objects.date import Date
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.club.domain.value_objects import Birthdate, Gender, License
from kwai.modules.teams.domain.team import TeamIdentifier
from kwai.modules.teams.domain.team_member import (
    MemberEntity,
    MemberIdentifier,
    TeamMember,
)
from kwai.modules.teams.repositories._tables import (
    CountryRow,
    MemberPersonRow,
    MemberRow,
    TeamMemberRow,
)


@dataclass(frozen=True, kw_only=True, slots=True)
class TeamMemberQueryRow(JoinedTableRow):
    """A data transfer object for the team member query."""

    team_member: TeamMemberRow
    member: MemberRow
    person: MemberPersonRow
    country: CountryRow

    def create_team_member(self) -> TeamMember:
        """Create a team member from a row."""
        return TeamMember(
            active=self.team_member.active == 1,
            member=MemberEntity(
                id_=MemberIdentifier(self.member.id),
                uuid=UniqueId.create_from_string(self.member.uuid),
                name=Name(
                    first_name=self.person.firstname, last_name=self.person.lastname
                ),
                license=License(
                    number=self.member.license,
                    end_date=Date.create_from_date(self.member.license_end_date),
                ),
                birthdate=Birthdate(Date.create_from_date(self.person.birthdate)),
                gender=Gender(self.person.gender),
                nationality=self.country.create_country(),
            ),
            traceable_time=TraceableTime(
                created_at=Timestamp(self.team_member.created_at),
                updated_at=Timestamp(self.team_member.updated_at),
            ),
        )


class TeamMemberDbQuery(DatabaseQuery):
    """A database query for getting team members."""

    def init(self):
        self._query.from_(TeamMemberRow.__table_name__).left_join(
            MemberRow.__table_name__,
            on(TeamMemberRow.column("member_id"), MemberRow.column("id")),
        ).join(
            MemberPersonRow.__table_name__,
            on(MemberRow.column("person_id"), MemberPersonRow.column("id")),
        ).inner_join(
            CountryRow.__table_name__,
            on(CountryRow.column("id"), MemberPersonRow.column("nationality_id")),
        )

    @property
    def columns(self):
        return TeamMemberQueryRow.get_aliases()

    def filter_by_teams(self, *ids: TeamIdentifier) -> Self:
        """Filter by teams.

        Only the rows that belong to the teams with the given ids, will be returned.
        """
        unpacked_ids = tuple(i.value for i in ids)
        self._query.and_where(TeamMemberRow.field("team_id").in_(*unpacked_ids))
        return self

    async def fetch_team_members(self) -> dict[TeamIdentifier, list[TeamMember]]:
        """Fetch team members.

        A specialized fetch method that already transforms the rows into TeamMember
        objects.

        Returns:
            A dictionary that contains the list of team members for each team.
            The key is the identifier of the team.
        """
        result: dict[TeamIdentifier, list[TeamMember]] = defaultdict(list)

        async for row in self.fetch():
            team_member_row = TeamMemberQueryRow.map(row)
            result[TeamIdentifier(team_member_row.team_member.team_id)].append(
                team_member_row.create_team_member()
            )

        return result
