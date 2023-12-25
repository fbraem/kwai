"""Module that defines a database query for coaches."""
from sql_smith.functions import on

from kwai.core.db.database_query import DatabaseQuery
from kwai.modules.training.coaches.coach import CoachIdentifier
from kwai.modules.training.coaches.coach_query import CoachQuery
from kwai.modules.training.coaches.coach_tables import CoachesTable, PersonsTable


class CoachDbQuery(DatabaseQuery, CoachQuery):
    """A database query for coaches."""

    @property
    def count_column(self) -> str:
        return CoachesTable.column("id")

    def init(self):
        self._query.from_(CoachesTable.table_name).columns(
            *(CoachesTable.aliases() + PersonsTable.aliases())
        ).join(
            PersonsTable.table_name,
            on(CoachesTable.column("person_id"), PersonsTable.column("id")),
        )

    @property
    def columns(self):
        return CoachesTable.aliases() + PersonsTable.aliases()

    def filter_by_ids(self, *ids: CoachIdentifier) -> "CoachQuery":
        unpacked_ids = tuple(i.value for i in ids)
        self._query.and_where(CoachesTable.field("id").in_(*unpacked_ids))
        return self

    def filter_by_id(self, id_: CoachIdentifier) -> "CoachQuery":
        self._query.and_where(CoachesTable.field("id").eq(id_.value))
        return self
