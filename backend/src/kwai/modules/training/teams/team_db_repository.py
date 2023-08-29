"""Module that defines a team repository for a database."""
from typing import AsyncIterator

from sql_smith.query import SelectQuery

from kwai.core.db.database import Database
from kwai.modules.training.teams.team import TeamEntity, TeamIdentifier
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

    def _create_query(self) -> SelectQuery:
        """Create the base select query."""
        return (
            self._database.create_query_factory()
            .select()
            .from_(TeamsTable.table_name)
            .columns(*TeamsTable.aliases())
        )

    async def get_by_ids(self, *ids: TeamIdentifier) -> AsyncIterator[TeamEntity]:
        unpacked_ids = tuple(i.value for i in ids)
        query = self._create_query().and_where(
            TeamsTable.field("id").in_(*unpacked_ids)
        )

        async for row in self._database.fetch(query):
            yield TeamsTable(row).create_entity()
