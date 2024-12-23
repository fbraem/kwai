"""Module that implements a training query for a database."""

from typing import AsyncIterator

from sql_smith.functions import alias, criteria, express, func, group, literal, on

from kwai.core.db.database import Database
from kwai.core.db.database_query import DatabaseQuery
from kwai.core.db.rows import OwnersTable
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.modules.training.coaches.coach import CoachEntity
from kwai.modules.training.teams.team import TeamEntity
from kwai.modules.training.teams.team_tables import TeamsTable
from kwai.modules.training.trainings.training import TrainingIdentifier
from kwai.modules.training.trainings.training_definition import TrainingDefinitionEntity
from kwai.modules.training.trainings.training_query import TrainingQuery
from kwai.modules.training.trainings.training_tables import (
    TrainingCoachRow,
    TrainingContentsTable,
    TrainingDefinitionsTable,
    TrainingsTable,
    TrainingTeamsTable,
)


class TrainingDbQuery(TrainingQuery, DatabaseQuery):
    """A database query for trainings."""

    def __init__(self, database: Database):
        self._main_query = database.create_query_factory().select()
        super().__init__(database)

    def init(self):
        # This query will be used as CTE, so only joins the tables that are needed
        # for counting and limiting results.
        self._query.from_(TrainingsTable.table_name).left_join(
            TrainingDefinitionsTable.table_name,
            on(
                TrainingsTable.column("definition_id"),
                TrainingDefinitionsTable.column("id"),
            ),
        )
        self._main_query = (
            self._main_query.from_(TrainingsTable.table_name)
            .columns(
                *(
                    self.columns
                    + TeamsTable.aliases()
                    + OwnersTable.aliases("definition_owners")
                    + TrainingContentsTable.aliases()
                    + OwnersTable.aliases()
                )
            )
            .with_("limited", self._query)
            .right_join("limited", on("limited.id", TrainingsTable.column("id")))
            .left_join(
                TrainingDefinitionsTable.table_name,
                on(
                    TrainingsTable.column("definition_id"),
                    TrainingDefinitionsTable.column("id"),
                ),
            )
            .left_join(
                alias(OwnersTable.table_name, "definition_owners"),
                on(TrainingDefinitionsTable.column("user_id"), "definition_owners.id"),
            )
            .left_join(
                TeamsTable.table_name,
                on(TeamsTable.column("id"), TrainingDefinitionsTable.column("team_id")),
            )
            .join(
                TrainingContentsTable.table_name,
                on(
                    TrainingContentsTable.column("training_id"),
                    TrainingsTable.column("id"),
                ),
            )
            .join(
                OwnersTable.table_name,
                on(OwnersTable.column("id"), TrainingContentsTable.column("user_id")),
            )
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
                    literal(month),
                )
            )
        self._query.and_where(group(condition))
        return self

    def filter_by_dates(self, start: Timestamp, end: Timestamp) -> "TrainingQuery":
        self._query.and_where(
            TrainingsTable.field("start_date").between(str(start), str(end))
        )
        return self

    def filter_by_coach(self, coach: CoachEntity) -> "TrainingQuery":
        inner_select = (
            self._database.create_query_factory()
            .select()
            .columns(TrainingCoachRow.column("training_id"))
            .from_(TrainingCoachRow.__table_name__)
            .where(TrainingCoachRow.field("coach_id").eq(coach.id.value))
        )
        condition = TrainingsTable.field("id").in_(express("{}", inner_select))
        self._query.and_where(group(condition))
        return self

    def filter_by_team(self, team: TeamEntity) -> "TrainingQuery":
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

    def fetch(
        self, limit: int | None = None, offset: int | None = None
    ) -> AsyncIterator[dict[str, any]]:
        self._query.limit(limit)
        self._query.offset(offset)
        self._query.columns(TrainingsTable.column("id"))
        self._main_query.order_by(TrainingsTable.column("id"))

        return self._database.fetch(self._main_query)

    def order_by_date(self) -> "TrainingQuery":
        self._query.order_by(TrainingsTable.column("start_date"), "ASC")
        self._main_query.order_by(TrainingsTable.column("start_date"), "ASC")
        return self
