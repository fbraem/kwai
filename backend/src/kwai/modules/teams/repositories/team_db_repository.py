"""Module that implements a team repository for a database."""

from dataclasses import dataclass
from typing import AsyncGenerator, Self

from sql_smith.functions import on

from kwai.core.db.database import Database
from kwai.core.db.database_query import DatabaseQuery
from kwai.core.db.table_row import JoinedTableRow
from kwai.core.domain.entity import Entity
from kwai.modules.club.repositories._tables import (
    CountryRow,
)
from kwai.modules.teams.domain.team import TeamEntity, TeamIdentifier
from kwai.modules.teams.repositories._tables import (
    MemberPersonRow,
    MemberRow,
    TeamMemberRow,
    TeamRow,
)
from kwai.modules.teams.repositories.team_repository import TeamQuery, TeamRepository


@dataclass(kw_only=True, frozen=True, slots=True)
class TeamQueryRow(JoinedTableRow):
    """A data transfer object for the team query."""

    team: TeamRow
    team_members: TeamMemberRow


class TeamDbQuery(TeamQuery, DatabaseQuery):
    """A team query for a database."""

    def __init__(self, database: Database):
        super().__init__(database)

    def init(self):
        self._query.from_(TeamRow.__table_name__).inner_join(
            TeamMemberRow.__table_name__,
            on(TeamMemberRow.column("team_id"), TeamRow.column("id")),
        ).inner_join(
            MemberRow.__table_name__,
            on(MemberRow.column("id"), TeamMemberRow.column("member_id")),
        ).inner_join(
            MemberPersonRow.__table_name__,
            on(MemberPersonRow.column("id"), MemberRow.column("person_id")),
        ).inner_join(
            CountryRow.__table_name__,
            on(CountryRow.column("id"), MemberPersonRow.column("nationality_id")),
        )

    @property
    def columns(self):
        pass

    def find_by_id(self, id_: TeamIdentifier) -> Self:
        pass


class TeamDbRepository(TeamRepository):
    """A team repository for a database."""

    def create_query(self) -> TeamQuery:
        pass

    async def get(self, query: TeamQuery | None = None) -> TeamEntity:
        pass

    def get_all(
        self,
        query: TeamQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncGenerator[TeamEntity, None]:
        pass

    def __init__(self, database: Database):
        self._database = database

    async def create(self, team: TeamEntity) -> TeamEntity:
        new_team_id = await self._database.insert(
            TeamRow.__table_name__, TeamRow.persist(team)
        )
        return Entity.replace(team, id_=TeamIdentifier(new_team_id))

    async def delete(self, team: TeamEntity) -> None:
        await self._database.delete(team.id.value, TeamRow.__table_name__)
