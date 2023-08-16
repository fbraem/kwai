"""Module that defines a coach repository for a database."""
from sql_smith.functions import on

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

    async def get_by_id(self, id: CoachIdentifier) -> CoachEntity:
        query = (
            self._database.create_query_factory()
            .select()
            .from_(CoachesTable.table_name)
            .columns(*(CoachesTable.aliases() + PersonsTable.aliases()))
            .join(
                PersonsTable.table_name,
                on(CoachesTable.column("person_id"), PersonsTable.column("id")),
            )
            .and_where(CoachesTable.field("id").eq(id.value))
        )

        row = await self._database.fetch_one(query)

        if not row:
            raise CoachNotFoundException(f"Coach with id {id} not found.")

        return _create_entity(CoachesTable(row), PersonsTable(row))
