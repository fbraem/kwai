"""Module that defines a database query to get coaches of training(s)."""
from collections import defaultdict

from sql_smith.functions import on

from kwai.core.db.database_query import DatabaseQuery
from kwai.core.db.rows import OwnersTable
from kwai.core.domain.value_objects.name import Name
from kwai.modules.training.trainings.training import TrainingIdentifier
from kwai.modules.training.trainings.training_tables import (
    CoachesTable,
    PersonsTable,
    TrainingCoachesTable,
)
from kwai.modules.training.trainings.value_objects import Coach, TrainingCoach


class TrainingCoachDbQuery(DatabaseQuery):
    """A database query for getting coaches of training(s)."""

    def init(self):
        self._query.from_(TrainingCoachesTable.table_name).left_join(
            CoachesTable.table_name,
            on(TrainingCoachesTable.column("coach_id"), CoachesTable.column("id")),
        ).join(
            PersonsTable.table_name,
            on(CoachesTable.column("person_id"), PersonsTable.column("id")),
        ).join(
            OwnersTable.table_name,
            on(CoachesTable.column("user_id"), OwnersTable.column("id")),
        )

    @property
    def columns(self):
        return (
            TrainingCoachesTable.aliases()
            + CoachesTable.aliases()
            + PersonsTable.aliases()
            + OwnersTable.aliases()
        )

    def filter_by_trainings(self, *ids: TrainingIdentifier) -> "TrainingCoachDbQuery":
        """Filter by trainings.

        Only the rows of the trainings with the given ids, will be returned.
        """
        unpacked_ids = tuple(i.value for i in ids)
        self._query.and_where(
            TrainingCoachesTable.field("training_id").in_(*unpacked_ids)
        )
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

        async for record in self.fetch():
            training_coach = TrainingCoachesTable(record)
            owner = OwnersTable(record).create_owner()
            coach = CoachesTable(record)
            person = PersonsTable(record)
            result[TrainingIdentifier(training_coach.training_id)].append(
                training_coach.create_coach(
                    Coach(
                        id=coach.id,
                        name=Name(
                            first_name=person.firstname, last_name=person.lastname
                        ),
                    ),
                    owner,
                )
            )
        return result
