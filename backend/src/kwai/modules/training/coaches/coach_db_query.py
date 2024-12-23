"""Module that defines a database query for coaches."""

from dataclasses import dataclass

from sql_smith.functions import on

from kwai.core.db.database_query import DatabaseQuery
from kwai.core.db.table_row import JoinedTableRow
from kwai.core.domain.value_objects.name import Name
from kwai.modules.training.coaches._tables import (
    CoachRow,
    MemberRow,
    PersonRow,
)
from kwai.modules.training.coaches.coach import CoachEntity, CoachIdentifier
from kwai.modules.training.coaches.coach_query import CoachQuery


@dataclass(kw_only=True, frozen=True, slots=True)
class CoachQueryRow(JoinedTableRow):
    """A data transfer object for the coach query."""

    member: MemberRow
    person: PersonRow
    coach: CoachRow

    def create_entity(self) -> CoachEntity:
        """Create a coach entity from a row."""
        return CoachEntity(
            id_=CoachIdentifier(self.coach.id),
            name=Name(first_name=self.person.firstname, last_name=self.person.lastname),
            active=self.coach.active == 1,
        )


class CoachDbQuery(DatabaseQuery, CoachQuery):
    """A database query for coaches."""

    @property
    def count_column(self) -> str:
        return CoachRow.column("id")

    def init(self):
        self._query.from_(CoachRow.__table_name__).join(
            MemberRow.__table_name__,
            on(MemberRow.column("id"), CoachRow.column("member_id")),
        ).inner_join(
            PersonRow.__table_name__,
            on(MemberRow.column("person_id"), PersonRow.column("id")),
        )

    @property
    def columns(self):
        return CoachQueryRow.get_aliases()

    def filter_by_ids(self, *ids: CoachIdentifier) -> "CoachQuery":
        unpacked_ids = tuple(i.value for i in ids)
        self._query.and_where(CoachRow.field("id").in_(*unpacked_ids))
        return self

    def filter_by_id(self, id_: CoachIdentifier) -> "CoachQuery":
        self._query.and_where(CoachRow.field("id").eq(id_.value))
        return self

    def filter_by_active(self) -> "CoachQuery":
        self._query.and_where(CoachRow.field("active").eq(1))
        return self
