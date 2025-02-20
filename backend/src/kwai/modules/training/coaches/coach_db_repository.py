"""Module that defines a coach repository for a database."""

from typing import AsyncIterator

from kwai.core.db.database import Database
from kwai.modules.training.coaches._tables import (
    CoachRow,
    PersonRow,
)
from kwai.modules.training.coaches.coach import CoachEntity, CoachIdentifier
from kwai.modules.training.coaches.coach_db_query import CoachDbQuery, CoachQueryRow
from kwai.modules.training.coaches.coach_query import CoachQuery
from kwai.modules.training.coaches.coach_repository import (
    CoachNotFoundException,
    CoachRepository,
)


def _create_entity(coach_row: CoachRow, person_row: PersonRow) -> CoachEntity:
    return coach_row.create_entity(person_row)


class CoachDbRepository(CoachRepository):
    """A coach repository for a database."""

    def __init__(self, database: Database):
        """Initialize the repository.

        Args:
            database: The database for this repository.
        """
        self._database = database

    def create_query(self) -> CoachQuery:
        """Create the coach query."""
        return CoachDbQuery(self._database)

    async def get_by_id(self, id: CoachIdentifier) -> CoachEntity:
        query = self.create_query().filter_by_id(id)
        row = await query.fetch_one()

        if not row:
            raise CoachNotFoundException(f"Coach with id {id} not found.")

        return CoachQueryRow.map(row).create_entity()

    async def get_by_ids(self, *ids: CoachIdentifier) -> AsyncIterator[CoachEntity]:
        query = self.create_query().filter_by_ids(*ids)

        async for row in query.fetch():
            yield CoachQueryRow.map(row).create_entity()

    async def get_all(
        self, query: CoachQuery | None = None
    ) -> AsyncIterator[CoachEntity]:
        query = query or self.create_query()
        async for row in query.fetch():
            yield CoachQueryRow.map(row).create_entity()
