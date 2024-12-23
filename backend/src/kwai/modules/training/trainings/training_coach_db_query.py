"""Module that defines a database query to get coaches of training(s)."""

from collections import defaultdict
from dataclasses import dataclass

from sql_smith.functions import on

from kwai.core.db.database_query import DatabaseQuery
from kwai.core.db.rows import OwnersTable, OwnerTableRow
from kwai.core.db.table_row import JoinedTableRow
from kwai.core.domain.value_objects.name import Name
from kwai.modules.training.coaches._tables import (  # noqa
    CoachRow,
    MemberRow,
    PersonRow,
)
from kwai.modules.training.coaches.coach import CoachEntity, CoachIdentifier
from kwai.modules.training.trainings.training import TrainingIdentifier
from kwai.modules.training.trainings.training_tables import (
    TrainingCoachRow,
)
from kwai.modules.training.trainings.value_objects import TrainingCoach


@dataclass(kw_only=True, frozen=True, slots=True)
class TrainingCoachQueryRow(JoinedTableRow):
    """A data transfer object for the training coach query."""

    training_coach: TrainingCoachRow
    member: MemberRow
    person: PersonRow
    coach: CoachRow
    owner: OwnerTableRow

    def create_coach(self) -> TrainingCoach:
        """Create a training coach from a row."""
        return TrainingCoach(
            coach=CoachEntity(
                id_=CoachIdentifier(self.coach.id),
                name=Name(
                    first_name=self.person.firstname, last_name=self.person.lastname
                ),
                active=self.coach.active == 1,
            ),
            owner=self.owner.create_owner(),
            present=self.training_coach.present == 1,
            type=self.training_coach.coach_type,
            payed=self.training_coach.payed == 1,
            remark=(
                "" if self.training_coach.remark is None else self.training_coach.remark
            ),
        )


class TrainingCoachDbQuery(DatabaseQuery):
    """A database query for getting coaches of training(s)."""

    def init(self):
        self._query.from_(TrainingCoachRow.__table_name__).left_join(
            CoachRow.__table_name__,
            on(TrainingCoachRow.column("coach_id"), CoachRow.column("id")),
        ).join(
            MemberRow.__table_name__,
            on(CoachRow.column("member_id"), MemberRow.column("id")),
        ).join(
            PersonRow.__table_name__,
            on(MemberRow.column("person_id"), PersonRow.column("id")),
        ).join(
            OwnersTable.table_name,
            on(CoachRow.column("user_id"), OwnerTableRow.column("id")),
        )

    @property
    def columns(self):
        return TrainingCoachQueryRow.get_aliases()

    def filter_by_trainings(self, *ids: TrainingIdentifier) -> "TrainingCoachDbQuery":
        """Filter by trainings.

        Only the rows of the trainings with the given ids, will be returned.
        """
        unpacked_ids = tuple(i.value for i in ids)
        self._query.and_where(TrainingCoachRow.field("training_id").in_(*unpacked_ids))
        return self

    async def fetch_coaches(self) -> dict[TrainingIdentifier, list[TrainingCoach]]:
        """Fetch coaches.

        A specialized fetch method that already transforms the records into
        TrainingCoach objects.

        Returns:
            A dictionary that contains the list of coaches for trainings. The key
            is the identifier of a training.
        """
        result: dict[TrainingIdentifier, list[TrainingCoach]] = defaultdict(list)

        async for row in self.fetch():
            training_coach_row = TrainingCoachQueryRow.map(row)
            result[
                TrainingIdentifier(training_coach_row.training_coach.training_id)
            ].append(training_coach_row.create_coach())
        return result
