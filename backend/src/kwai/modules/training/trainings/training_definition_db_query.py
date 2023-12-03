"""Module that implements a TrainingDefinitionQuery for a database."""
from sql_smith.functions import on

from kwai.core.db.database_query import DatabaseQuery
from kwai.core.db.rows import OwnersTable
from kwai.modules.training.teams.team_tables import TeamsTable
from kwai.modules.training.trainings.training_definition import (
    TrainingDefinitionIdentifier,
)
from kwai.modules.training.trainings.training_definition_query import (
    TrainingDefinitionQuery,
)
from kwai.modules.training.trainings.training_tables import (
    TrainingDefinitionsTable,
)


class TrainingDefinitionDbQuery(DatabaseQuery, TrainingDefinitionQuery):
    """A database query for a training definition."""

    def init(self):
        return (
            self._query.from_(TrainingDefinitionsTable.table_name)
            .join(
                OwnersTable.table_name,
                on(
                    OwnersTable.column("id"), TrainingDefinitionsTable.column("user_id")
                ),
            )
            .left_join(
                TeamsTable.table_name,
                on(TeamsTable.column("id"), TrainingDefinitionsTable.column("team_id")),
            )
        )

    @property
    def columns(self):
        return (
            TrainingDefinitionsTable.aliases()
            + TeamsTable.aliases()
            + OwnersTable.aliases()
        )

    @property
    def count_column(self) -> str:
        return TrainingDefinitionsTable.column("id")

    def filter_by_id(
        self, id_: TrainingDefinitionIdentifier
    ) -> TrainingDefinitionQuery:
        self._query.and_where(TrainingDefinitionsTable.field("id").eq(id_.value))
        return self

    def filter_by_ids(
        self, *ids: TrainingDefinitionIdentifier
    ) -> "TrainingDefinitionQuery":
        unpacked_ids = (id_.value for id_ in ids)
        self._query.and_where(TrainingDefinitionsTable.field("id").in_(*unpacked_ids))
        return self
