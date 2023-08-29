"""Module that defines a coach repository for a database."""
from typing import AsyncIterator

from sql_smith.functions import on
from sql_smith.query import SelectQuery

from kwai.core.db.database import Database
from kwai.modules.training.coaches.coach import CoachEntity, CoachIdentifier
from kwai.modules.training.coaches.coach_repository import (
    CoachNotFoundException,
    CoachRepository,
)
from kwai.modules.training.coaches.coach_tables import (
    CoachesTable,
    CoachRow,
    PersonRow,
    PersonsTable,
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

    def _create_query(self) -> SelectQuery:
        """Create the base select query."""
        return (
            self._database.create_query_factory()
            .select()
            .from_(CoachesTable.table_name)
            .columns(*(CoachesTable.aliases() + PersonsTable.aliases()))
            .join(
                PersonsTable.table_name,
                on(CoachesTable.column("person_id"), PersonsTable.column("id")),
            )
        )

    async def get_by_id(self, id: CoachIdentifier) -> CoachEntity:
        query = self._create_query().and_where(CoachesTable.field("id").eq(id.value))
        row = await self._database.fetch_one(query)

        if not row:
            raise CoachNotFoundException(f"Coach with id {id} not found.")

        return _create_entity(CoachesTable(row), PersonsTable(row))

    async def get_by_ids(self, *ids: CoachIdentifier) -> AsyncIterator[CoachEntity]:
        unpacked_ids = tuple(i.value for i in ids)
        query = self._create_query().and_where(
            CoachesTable.field("id").in_(*unpacked_ids)
        )

        async for row in self._database.fetch(query):
            yield _create_entity(CoachesTable(row), PersonsTable(row))
