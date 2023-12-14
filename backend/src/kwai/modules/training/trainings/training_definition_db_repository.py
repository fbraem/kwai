"""Module that implements a training definition repository for a database."""


from typing import Any, AsyncIterator

from kwai.core.db.database import Database
from kwai.core.db.rows import OwnersTable
from kwai.core.domain.entity import Entity
from kwai.modules.training.teams.team_tables import TeamsTable
from kwai.modules.training.trainings.training_definition import (
    TrainingDefinitionEntity,
    TrainingDefinitionIdentifier,
)
from kwai.modules.training.trainings.training_definition_db_query import (
    TrainingDefinitionDbQuery,
)
from kwai.modules.training.trainings.training_definition_query import (
    TrainingDefinitionQuery,
)
from kwai.modules.training.trainings.training_definition_repository import (
    TrainingDefinitionNotFoundException,
    TrainingDefinitionRepository,
)
from kwai.modules.training.trainings.training_tables import (
    TrainingDefinitionRow,
    TrainingDefinitionsTable,
)


def _create_entity(row: dict[str, Any]):
    if row[TrainingDefinitionsTable.alias_name("team_id")] is None:
        team = None
    else:
        team = TeamsTable(row).create_entity()
    return TrainingDefinitionsTable(row).create_entity(
        team=team, owner=OwnersTable(row).create_owner()
    )


class TrainingDefinitionDbRepository(TrainingDefinitionRepository):
    """A training definition repository for a database."""

    def __init__(self, database: Database) -> None:
        """Initialize the repository.

        Args:
            database: The database for this repository
        """
        self._database = database

    def create_query(self) -> TrainingDefinitionQuery:  # noqa
        return TrainingDefinitionDbQuery(self._database)

    async def get_by_id(
        self, id_: TrainingDefinitionIdentifier
    ) -> TrainingDefinitionEntity:
        query = self.create_query()
        query.filter_by_id(id_)

        if row := await query.fetch_one():
            return _create_entity(row)

        raise TrainingDefinitionNotFoundException(
            f"Training definition with id {id_} does not exist."
        )

    async def get_all(
        self,
        query: TrainingDefinitionQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncIterator[TrainingDefinitionEntity]:
        if query is None:
            query = self.create_query()
        async for row in query.fetch(limit, offset):
            yield _create_entity(row)

    async def create(
        self, training_definition: TrainingDefinitionEntity
    ) -> TrainingDefinitionEntity:
        new_id = await self._database.insert(
            TrainingDefinitionsTable.table_name,
            TrainingDefinitionRow.persist(training_definition),
        )
        await self._database.commit()
        return Entity.replace(
            training_definition, id_=TrainingDefinitionIdentifier(new_id)
        )

    async def update(self, training_definition: TrainingDefinitionEntity):
        await self._database.update(
            training_definition.id.value,
            TrainingDefinitionsTable.table_name,
            TrainingDefinitionRow.persist(training_definition),
        )
        await self._database.commit()

    async def delete(self, training_definition: TrainingDefinitionEntity):
        await self._database.delete(
            training_definition.id.value, TrainingDefinitionsTable.table_name
        )
        await self._database.commit()
