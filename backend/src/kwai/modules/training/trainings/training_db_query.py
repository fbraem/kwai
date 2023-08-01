"""Module that implements a training query for a database."""
from datetime import datetime

from sql_smith.functions import criteria, express, func, group, literal, on

from kwai.core.db.database_query import DatabaseQuery
from kwai.modules.training.trainings.training import TrainingIdentifier
from kwai.modules.training.trainings.training_definition import TrainingDefinitionEntity
from kwai.modules.training.trainings.training_query import TrainingQuery
from kwai.modules.training.trainings.training_tables import (
    TrainingCoachesTable,
    TrainingDefinitionsTable,
    TrainingsTable,
    TrainingTeamsTable,
)
from kwai.modules.training.trainings.value_objects import Coach, Team


class TrainingDbQuery(TrainingQuery, DatabaseQuery):
    """A database query for trainings."""

    def init(self):
        self._query.from_(TrainingsTable.table_name).left_join(
            TrainingDefinitionsTable.table_name,
            on(
                TrainingsTable.column("definition_id"),
                TrainingDefinitionsTable.column("id"),
            ),
        )

    @property
    def columns(self):
        return TrainingsTable.aliases() + TrainingDefinitionsTable.aliases()

    @property
    def count_column(self) -> str:
        return TrainingsTable.column("id")

    def filter_by_id(self, id_: TrainingIdentifier) -> "TrainingQuery":
        self._query.and_where(TrainingsTable.field("id").eq(id_.value))
        return self

    def filter_by_year_month(
        self, year: int, month: int | None = None
    ) -> "TrainingQuery":
        condition = criteria(
            "{} = {}", func("YEAR", TrainingsTable.column("start_date")), literal(year)
        )
        if month is not None:
            condition = condition.and_(
                criteria(
                    "{} = {}",
                    func("MONTH", TrainingsTable.column("start_date")),
                    literal(year),
                )
            )
        self._query.and_where(group(condition))
        return self

    def filter_by_dates(self, start: datetime, end: datetime) -> "TrainingQuery":
        self._query.and_where(TrainingsTable.field("start_date").between(start, end))
        return self

    def filter_by_coach(self, coach: Coach) -> "TrainingQuery":
        inner_select = (
            self._database.create_query_factory()
            .select()
            .columns(TrainingCoachesTable.column("training_id"))
            .from_(TrainingCoachesTable.table_name)
            .where(TrainingCoachesTable.field("coach_id").eq(coach.id.value))
        )
        condition = TrainingsTable.field("id").in_(express("{}", inner_select))
        self._query.and_where(group(condition))
        return self

    def filter_by_team(self, team: Team) -> "TrainingQuery":
        inner_select = (
            self._database.create_query_factory()
            .select()
            .columns(TrainingTeamsTable.column("training_id"))
            .from_(TrainingTeamsTable.table_name)
            .where(TrainingTeamsTable.field("team_id").eq(team.id.value))
        )
        condition = TrainingsTable.field("id").in_(express("{}", inner_select))
        self._query.and_where(group(condition))
        return self

    def filter_by_definition(
        self, definition: TrainingDefinitionEntity
    ) -> "TrainingQuery":
        self._query.and_where(
            TrainingsTable.field("definition_id").eq(definition.id.value)
        )
        return self

    def filter_active(self) -> "TrainingQuery":
        self._query.and_where(TrainingsTable.field("active").eq(1))
        return self
