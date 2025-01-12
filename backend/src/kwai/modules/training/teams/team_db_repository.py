"""Module that defines a team repository for a database."""

from typing import AsyncIterator

from kwai.core.db.database import Database
from kwai.modules.training.teams.team import TeamEntity, TeamIdentifier
from kwai.modules.training.teams.team_db_query import TeamDbQuery
from kwai.modules.training.teams.team_query import TeamQuery
from kwai.modules.training.teams.team_repository import TeamRepository
from kwai.modules.training.teams.team_tables import TeamsTable


class TeamDbRepository(TeamRepository):
    """A team repository for a database."""

    def __init__(self, database: Database):
        """Initialize the repository.

        Args:
            database: The database for this repository.
        """
        self._database = database

    def create_query(self) -> TeamQuery:
        """Create the team query."""
        return TeamDbQuery(self._database)

    async def get_by_id(self, id: TeamIdentifier) -> TeamEntity:
        query = self.create_query()
        query.filter_by_id(id)

        row = await query.fetch_one()

        return TeamsTable(row).create_entity()

    async def get_all(self) -> AsyncIterator[TeamEntity]:
        query = self.create_query()
        async for row in query.fetch():
            yield TeamsTable(row).create_entity()

    async def get_by_ids(self, *ids: TeamIdentifier) -> AsyncIterator[TeamEntity]:
        query = self.create_query()
        query.filter_by_ids(*ids)

        async for row in query.fetch():
            yield TeamsTable(row).create_entity()
