"""Module for implementing a training repository for a database."""
from typing import AsyncIterator

from sql_smith.functions import alias, express, field

from kwai.core.db.database import Database, Record
from kwai.core.db.rows import OwnersTable
from kwai.core.domain.entity import Entity
from kwai.modules.training.teams.team import TeamEntity
from kwai.modules.training.trainings.training import TrainingEntity, TrainingIdentifier
from kwai.modules.training.trainings.training_coach_db_query import TrainingCoachDbQuery
from kwai.modules.training.trainings.training_db_query import TrainingDbQuery
from kwai.modules.training.trainings.training_definition import TrainingDefinitionEntity
from kwai.modules.training.trainings.training_query import TrainingQuery
from kwai.modules.training.trainings.training_repository import (
    TrainingNotFoundException,
    TrainingRepository,
)
from kwai.modules.training.trainings.training_tables import (
    TrainingCoachesTable,
    TrainingCoachRow,
    TrainingContentRow,
    TrainingContentsTable,
    TrainingDefinitionsTable,
    TrainingRow,
    TrainingsTable,
    TrainingTeamRow,
    TrainingTeamsTable,
)
from kwai.modules.training.trainings.training_team_db_query import TrainingTeamDbQuery
from kwai.modules.training.trainings.value_objects import TrainingCoach


def _create_entity(rows: list[Record]) -> TrainingEntity:
    """Create a training entity from a group of rows."""
    if rows[0][TrainingDefinitionsTable.alias_name("id")] is None:
        definition = None
    else:
        definition = TrainingDefinitionsTable(rows[0]).create_entity(
            OwnersTable(rows[0], "definition_owners").create_owner()
        )
    return TrainingsTable(rows[0]).create_entity(
        [
            TrainingContentsTable(row).create_content(OwnersTable(row).create_owner())
            for row in rows
        ],
        definition=definition,
    )


class TrainingDbRepository(TrainingRepository):
    """A training repository for a database."""

    def __init__(self, database: Database):
        """Initialize the repository.

        Args:
            database: The database for this repository.
        """
        self._database = database

    def create_query(self) -> TrainingQuery:
        return TrainingDbQuery(self._database)

    async def get_by_id(self, id: TrainingIdentifier) -> TrainingEntity:
        query = self.create_query()
        query.filter_by_id(id)

        try:
            row_iterator = self.get_all(query, 1)
            entity = await anext(row_iterator)
        except StopAsyncIteration:
            raise TrainingNotFoundException(
                f"Training with id {id} does not exist"
            ) from None
        return entity

    async def get_all(
        self,
        training_query: TrainingQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncIterator[TrainingEntity] | None:
        if training_query is None:
            training_query = self.create_query()

        trainings: dict[TrainingIdentifier, TrainingEntity] = {}
        group_by_column = TrainingsTable.alias_name("id")

        row_it = training_query.fetch(limit, offset)
        # Handle the first row
        try:
            record = await anext(row_it)
        except StopAsyncIteration:
            return

        group = [record]
        current_key = record[group_by_column]

        # Process all other rows
        async for record in row_it:
            new_key = record[group_by_column]
            if new_key != current_key:
                training = _create_entity(group)
                trainings[training.id] = training
                group = [record]
                current_key = new_key
            else:
                group.append(record)

        training = _create_entity(group)
        trainings[training.id] = training

        # Get the coaches of all the trainings.
        training_query = TrainingCoachDbQuery(self._database).filter_by_trainings(
            *trainings.keys()
        )
        coaches: dict[
            TrainingIdentifier, list[TrainingCoach]
        ] = await training_query.fetch_coaches()

        # Get the teams of all trainings
        team_query = TrainingTeamDbQuery(self._database).filter_by_trainings(
            *trainings.keys()
        )
        teams: dict[
            TrainingIdentifier, list[TeamEntity]
        ] = await team_query.fetch_teams()

        for training in trainings.values():
            training_coaches = coaches.get(training.id, [])
            training_teams = teams.get(training.id, [])
            if len(training_coaches) > 0 or len(training_teams) > 0:
                yield Entity.replace(
                    training, coaches=training_coaches, teams=training_teams
                )
            else:
                yield training

    async def create(self, training: TrainingEntity) -> TrainingEntity:
        new_id = await self._database.insert(
            TrainingsTable.table_name, TrainingRow.persist(training)
        )
        result = Entity.replace(training, id_=TrainingIdentifier(new_id))

        content_rows = [
            TrainingContentRow.persist(result, content) for content in training.texts
        ]

        await self._database.insert(TrainingContentsTable.table_name, *content_rows)
        await self._insert_coaches(result)
        await self._insert_teams(result)

        await self._database.commit()

        return result

    async def update(self, training: TrainingEntity) -> None:
        # Update the training
        await self._database.update(
            training.id.value,
            TrainingsTable.table_name,
            TrainingRow.persist(training),
        )

        # Update the text, first delete, then insert again.
        await self._delete_contents(training)
        content_rows = [
            TrainingContentRow.persist(training, content) for content in training.texts
        ]
        await self._database.insert(TrainingContentsTable.table_name, *content_rows)

        # Update coaches, first delete, then insert again.
        await self._delete_coaches(training)
        await self._insert_coaches(training)

        # Update teams, first delete, then insert again.
        await self._delete_teams(training)
        await self._insert_teams(training)

        await self._database.commit()

    async def _insert_coaches(self, training: TrainingEntity):
        """Insert the related coaches."""
        training_coach_rows = [
            TrainingCoachRow.persist(training, training_coach)
            for training_coach in training.coaches
        ]
        if training_coach_rows:
            await self._database.insert(
                TrainingCoachesTable.table_name, *training_coach_rows
            )

    async def _insert_teams(self, training: TrainingEntity):
        """Insert the related teams."""
        training_team_rows = [
            TrainingTeamRow.persist(training, team) for team in training.teams
        ]
        if training_team_rows:
            await self._database.insert(
                TrainingTeamsTable.table_name, *training_team_rows
            )

    async def _delete_coaches(self, training: TrainingEntity):
        """Delete coaches of the training."""
        delete_coaches_query = (
            self._database.create_query_factory()
            .delete(TrainingCoachesTable.table_name)
            .where(field("training_id").eq(training.id.value))
        )
        await self._database.execute(delete_coaches_query)

    async def _delete_contents(self, training: TrainingEntity):
        """Delete text contents of the training."""
        delete_contents_query = (
            self._database.create_query_factory()
            .delete(TrainingContentsTable.table_name)
            .where(field("training_id").eq(training.id.value))
        )
        await self._database.execute(delete_contents_query)

    async def _delete_teams(self, training: TrainingEntity):
        """Delete the teams of the training."""
        delete_teams_query = (
            self._database.create_query_factory()
            .delete(TrainingTeamsTable.table_name)
            .where(field("training_id").eq(training.id.value))
        )
        await self._database.execute(delete_teams_query)

    async def delete(self, training: TrainingEntity) -> None:
        await self._database.delete(training.id.value, TrainingsTable.table_name)

        await self._delete_contents(training),
        await self._delete_coaches(training),
        await self._delete_teams(training),

        await self._database.commit()

    async def reset_definition(
        self, training_definition: TrainingDefinitionEntity, delete: bool = False
    ) -> None:
        trainings_query = (
            self._database.create_query_factory()
            .select(TrainingsTable.column("id"))
            .from_(TrainingsTable.table_name)
            .and_where(field("definition_id").eq(training_definition.id.value))
        )
        if delete:
            delete_teams = (
                self._database.create_query_factory()
                .delete(TrainingTeamsTable.table_name)
                .and_where(TrainingTeamsTable.field("training_id").in_(trainings_query))
            )
            await self._database.execute(delete_teams)

            delete_coaches = (
                self._database.create_query_factory()
                .delete(TrainingCoachesTable.table_name)
                .and_where(
                    TrainingCoachesTable.field("training_id").in_(trainings_query)
                )
            )
            await self._database.execute(delete_coaches)

            delete_contents = (
                self._database.create_query_factory()
                .delete(TrainingContentsTable.table_name)
                .and_where(
                    TrainingContentsTable.field("training_id").in_(trainings_query)
                )
            )
            await self._database.execute(delete_contents)
            await self._database.commit()
        else:
            # Because it is not allowed to update the table that is used
            # in a sub query, we need to create a copy.
            copy_trainings_query = (
                self._database.create_query_factory()
                .select("t.id")
                .from_(alias(express("({})", trainings_query), "t"))
            )
            update_trainings = (
                self._database.create_query_factory()
                .update(TrainingsTable.table_name, {"definition_id": None})
                .where(TrainingsTable.field("id").in_(copy_trainings_query))
            )
            await self._database.execute(update_trainings)
            await self._database.commit()
