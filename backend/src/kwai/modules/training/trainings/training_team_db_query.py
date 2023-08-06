"""Module that defines a database query to get teams of training(s)."""
from collections import defaultdict

from sql_smith.functions import on

from kwai.core.db.database_query import DatabaseQuery
from kwai.modules.training.trainings.training import TrainingIdentifier
from kwai.modules.training.trainings.training_tables import (
    TeamsTable,
    TrainingTeamsTable,
)
from tests.core.test_jsonapi import Team


class TrainingTeamDbQuery(DatabaseQuery):
    """A database query for getting teams of training(s)."""

    def init(self):
        self._query.from_(TrainingTeamsTable.table_name).left_join(
            TeamsTable.table_name,
            on(TrainingTeamsTable.column("team_id"), TeamsTable.column("id")),
        )

    @property
    def columns(self):
        return TrainingTeamsTable.aliases() + TeamsTable.aliases()

    def filter_by_trainings(self, *ids: TrainingIdentifier) -> "TrainingTeamDbQuery":
        """Filter by trainings.

        Only the rows of the trainings with the given ids, will be returned.
        """
        unpacked_ids = tuple(i.value for i in ids)
        self._query.and_where(
            TrainingTeamsTable.field("training_id").in_(*unpacked_ids)
        )
        return self

    async def fetch_teams(self) -> dict[TrainingIdentifier, list[Team]]:
        """Fetch teams.

        A specialized fetch method that already transforms the records into
        Team objects.

        Returns:
            A dictionary that contains the list of teams for trainings. The key
            is the identifier of a training.
        """
        result: dict[TrainingIdentifier, list[Team]] = defaultdict(list)

        async for team_record in self.fetch():
            training_team = TrainingTeamsTable(team_record)
            result[TrainingIdentifier(training_team.training_id)].append(
                TeamsTable(team_record).create_team()
            )

        return result
