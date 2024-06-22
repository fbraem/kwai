"""Module for defining a team member repository for a database."""

from dataclasses import dataclass
from typing import AsyncGenerator, Self

from sql_smith.functions import on

from kwai.core.db.database import Database
from kwai.core.db.database_query import DatabaseQuery
from kwai.core.db.table_row import JoinedTableRow
from kwai.core.domain.value_objects.date import Date
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.club.domain.value_objects import Birthdate, Gender, License
from kwai.modules.teams.domain.team_member import MemberEntity, MemberIdentifier
from kwai.modules.teams.repositories._tables import (
    CountryRow,
    MemberPersonRow,
    MemberRow,
)
from kwai.modules.teams.repositories.member_repository import (
    MemberNotFoundException,
    MemberQuery,
    MemberRepository,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class MemberQueryRow(JoinedTableRow):
    """A data transfer object for the member query."""

    member: MemberRow
    person: MemberPersonRow
    country: CountryRow

    def create_entity(self) -> MemberEntity:
        """Create a team member entity from a row."""
        return MemberEntity(
            id_=MemberIdentifier(self.member.id),
            uuid=UniqueId.create_from_string(self.member.uuid),
            name=Name(first_name=self.person.firstname, last_name=self.person.lastname),
            license=License(
                number=self.member.license,
                end_date=Date.create_from_date(self.member.license_end_date),
            ),
            birthdate=Birthdate(Date.create_from_date(self.person.birthdate)),
            gender=Gender(self.person.gender),
            nationality=self.country.create_country(),
        )


class MemberDbQuery(MemberQuery, DatabaseQuery):
    """A team member query for a database."""

    def __init__(self, database: Database):
        super().__init__(database)

    def init(self):
        self._query.from_(MemberRow.__table_name__).inner_join(
            MemberPersonRow.__table_name__,
            on(MemberPersonRow.column("id"), MemberRow.column("person_id")),
        ).inner_join(
            CountryRow.__table_name__,
            on(CountryRow.column("id"), MemberPersonRow.column("nationality_id")),
        )

    @property
    def columns(self):
        return MemberQueryRow.get_aliases()

    def count_column(self):
        return MemberRow.column("id")

    def find_by_id(self, id_: MemberIdentifier) -> Self:
        self._query.and_where(MemberRow.field("id").eq(id_.value))
        return self

    def find_by_birthdate(self, start_date: Date, end_date: Date | None = None) -> Self:
        if end_date is None:
            self._query.and_where(MemberPersonRow.field("birthdate").gte(start_date))
        else:
            self._query.and_where(
                MemberPersonRow.field("birthdate").between(start_date, end_date)
            )
        return self


class MemberDbRepository(MemberRepository):
    """A member repository for a database."""

    def __init__(self, database: Database):
        self._database = database

    def create_query(self) -> MemberQuery:
        return MemberDbQuery(self._database)

    async def get(self, query: MemberQuery | None = None) -> MemberEntity:
        team_member_iterator = self.get_all(query)
        try:
            return await anext(team_member_iterator)
        except StopAsyncIteration:
            raise MemberNotFoundException("Member not found") from None

    async def get_all(
        self,
        query: MemberQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncGenerator[MemberEntity, None]:
        query = query or self.create_query()

        async for row in query.fetch(limit, offset):
            yield MemberQueryRow.map(row).create_entity()
