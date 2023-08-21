"""Module for implementing a training repository for a database."""
from typing import AsyncIterator

from kwai.core.db.database import Database, Record
from kwai.core.db.rows import OwnersTable
from kwai.core.domain.entity import Entity
from kwai.modules.training.trainings.training import TrainingEntity, TrainingIdentifier
from kwai.modules.training.trainings.training_coach_db_query import TrainingCoachDbQuery
from kwai.modules.training.trainings.training_db_query import TrainingDbQuery
from kwai.modules.training.trainings.training_query import TrainingQuery
from kwai.modules.training.trainings.training_repository import (
    TrainingNotFoundException,
    TrainingRepository,
)
from kwai.modules.training.trainings.training_tables import (
    TrainingContentsTable,
    TrainingDefinitionsTable,
    TrainingsTable,
)
from kwai.modules.training.trainings.training_team_db_query import TrainingTeamDbQuery
from kwai.modules.training.trainings.value_objects import Team, TrainingCoach


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
        teams: dict[TrainingIdentifier, list[Team]] = await team_query.fetch_teams()

        for training in trainings.values():
            training_coaches = coaches.get(training.id, [])
            training_teams = teams.get(training.id, [])
            if len(training_coaches) > 0 or len(training_teams) > 0:
                yield Entity.replace(
                    training, coaches=training_coaches, teams=training_teams
                )
            else:
                yield training
