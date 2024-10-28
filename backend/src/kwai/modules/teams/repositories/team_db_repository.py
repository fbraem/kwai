"""Module that implements a team repository for a database."""

from dataclasses import dataclass
from typing import Any, AsyncGenerator, Self

from sql_smith.functions import field, on

from kwai.core.db.database import Database
from kwai.core.db.database_query import DatabaseQuery
from kwai.core.db.table_row import JoinedTableRow
from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.date import Date
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.core.functions import async_groupby
from kwai.modules.club.domain.value_objects import Birthdate, Gender, License
from kwai.modules.teams.domain.team import TeamEntity, TeamIdentifier
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
    TeamRow,
)
from kwai.modules.teams.repositories.team_repository import (
    TeamNotFoundException,
    TeamQuery,
    TeamRepository,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class MemberPersonCountryMixin:
    """Dataclass for a member related row."""

    member: MemberRow
    member_person: MemberPersonRow
    country: CountryRow

    def create_member_entity(self) -> MemberEntity:
        """Create a member entity from a row."""
        return MemberEntity(
            id_=MemberIdentifier(self.member.id),
            name=Name(
                first_name=self.member_person.firstname,
                last_name=self.member_person.lastname,
            ),
            license=License(
                number=self.member.license,
                end_date=Date.create_from_date(self.member.license_end_date),
            ),
            birthdate=Birthdate(
                date=Date.create_from_date(self.member_person.birthdate)
            ),
            nationality=self.country.create_country(),
            gender=Gender(self.member_person.gender),
            uuid=UniqueId.create_from_string(self.member.uuid),
            active_in_club=self.member.active == 1,
        )


@dataclass(kw_only=True, frozen=True, slots=True)
class TeamQueryRow(MemberPersonCountryMixin, JoinedTableRow):
    """A data transfer object for the team query."""

    team: TeamRow
    team_member: TeamMemberRow

    @classmethod
    def create_entity(cls, rows: list[dict[str, Any]]) -> TeamEntity:
        """Create a team entity from a group of rows."""
        team_query_row = cls.map(rows[0])
        team_members = {}
        for row in rows:
            mapped_row = cls.map(row)
            if mapped_row.member.id is None:
                continue

            member = mapped_row.create_member_entity()
            team_members[member.uuid] = mapped_row.team_member.create_team_member(
                member
            )
        return team_query_row.team.create_entity(team_members)


class TeamDbQuery(TeamQuery, DatabaseQuery):
    """A team query for a database."""

    def __init__(self, database: Database):
        super().__init__(database)

    def init(self):
        self._query.from_(TeamRow.__table_name__).left_join(
            TeamMemberRow.__table_name__,
            on(TeamRow.column("id"), TeamMemberRow.column("team_id")),
        ).left_join(
            MemberRow.__table_name__,
            on(MemberRow.column("id"), TeamMemberRow.column("member_id")),
        ).left_join(
            MemberPersonRow.__table_name__,
            on(MemberPersonRow.column("id"), MemberRow.column("person_id")),
        ).left_join(
            CountryRow.__table_name__,
            on(CountryRow.column("id"), MemberPersonRow.column("nationality_id")),
        )

    @property
    def columns(self):
        return TeamQueryRow.get_aliases()

    @property
    def count_column(self) -> str:
        return TeamRow.column("id")

    def filter_by_id(self, id_: TeamIdentifier) -> Self:
        self._query.and_where(TeamRow.field("id").eq(id_.value))
        return self


class TeamDbRepository(TeamRepository):
    """A team repository for a database."""

    def create_query(self) -> TeamQuery:
        return TeamDbQuery(self._database)

    async def get(self, query: TeamQuery | None = None) -> TeamEntity:
        team_iterator = self.get_all(query)
        try:
            return await anext(team_iterator)
        except StopAsyncIteration:
            raise TeamNotFoundException("Team not found") from None

    async def get_all(
        self,
        query: TeamQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncGenerator[TeamEntity, None]:
        if query is None:
            query = self.create_query()

        group_by_column = "team_id"
        row_iterator = query.fetch(limit=limit, offset=offset)
        async for _, group in async_groupby(
            row_iterator, key=lambda row: row[group_by_column]
        ):
            yield TeamQueryRow.create_entity(group)

    def __init__(self, database: Database):
        self._database = database

    async def create(self, team: TeamEntity) -> TeamEntity:
        new_team_id = await self._database.insert(
            TeamRow.__table_name__, TeamRow.persist(team)
        )
        return Entity.replace(team, id_=TeamIdentifier(new_team_id))

    async def delete(self, team: TeamEntity) -> None:
        delete_team_members_query = (
            self._database.create_query_factory()
            .delete(TeamMemberRow.__table_name__)
            .where(field("team_id").eq(team.id.value))
        )
        await self._database.execute(delete_team_members_query)
        await self._database.delete(team.id.value, TeamRow.__table_name__)

    async def update(self, team: TeamEntity):
        await self._database.update(
            team.id.value, TeamRow.__table_name__, TeamRow.persist(team)
        )

    async def add_team_member(self, team: TeamEntity, member: TeamMember):
        team_member_row = TeamMemberRow.persist(team, member)
        await self._database.insert(TeamMemberRow.__table_name__, team_member_row)
