"""Module for defining a team member repository for a database."""

from dataclasses import dataclass
from typing import AsyncGenerator

from sql_smith.functions import on

from kwai.core.db.database import Database
from kwai.core.db.database_query import DatabaseQuery
from kwai.core.db.table_row import JoinedTableRow
from kwai.core.domain.value_objects.date import Date
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.club.domain.team_member import TeamMemberEntity, TeamMemberIdentifier
from kwai.modules.club.domain.value_objects import Gender, License
from kwai.modules.club.repositories._tables import (
    CountryRow,
    TeamMemberPersonRow,
    TeamMemberRow,
)
from kwai.modules.club.repositories.team_member_repository import (
    TeamMemberQuery,
    TeamMemberRepository,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class TeamMemberQueryRow(JoinedTableRow):
    """A data transfer object for the team member query."""

    member: TeamMemberRow
    person: TeamMemberPersonRow
    country: CountryRow

    def create_entity(self) -> TeamMemberEntity:
        """Create a team member entity from a row."""
        return TeamMemberEntity(
            id_=TeamMemberIdentifier(self.member.id),
            uuid=UniqueId.create_from_string(self.member.uuid),
            name=Name(first_name=self.person.firstname, last_name=self.person.lastname),
            license=License(
                number=self.member.license,
                end_date=Date.create_from_date(self.member.license_end_date),
            ),
            birthdate=Date.create_from_date(self.person.birthdate),
            gender=Gender(self.person.gender),
            nationality=self.country.create_country(),
        )


class TeamMemberDbQuery(TeamMemberQuery, DatabaseQuery):
    """A team member query for a database."""

    def __init__(self, database: Database):
        super().__init__(database)

    def init(self):
        self._query.from_(TeamMemberRow.__table_name__).inner_join(
            TeamMemberPersonRow.__table_name__,
            on(TeamMemberPersonRow.column("id"), TeamMemberRow.column("person_id")),
        ).inner_join(
            CountryRow.__table_name__,
            on(CountryRow.column("id"), TeamMemberPersonRow.column("nationality_id")),
        )

    @property
    def columns(self):
        return TeamMemberQueryRow.get_aliases()

    def count_column(self):
        return TeamMemberRow.column("id")


class TeamMemberDbRepository(TeamMemberRepository):
    """A team member repository for a database."""

    def __init__(self, database: Database):
        self._database = database

    def create_query(self) -> TeamMemberQuery:
        return TeamMemberDbQuery(self._database)

    async def get(self, query: TeamMemberQuery | None = None) -> TeamMemberEntity:
        pass

    async def get_all(
        self,
        query: TeamMemberQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncGenerator[TeamMemberEntity, None]:
        query = query or self.create_query()

        async for row in query.fetch(limit, offset):
            yield TeamMemberQueryRow.map(row).create_entity()
