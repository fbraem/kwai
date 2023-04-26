"""Module that implements an application repository for a database."""
from typing import AsyncIterator

from kwai.core.db.database import Database
from kwai.core.domain.entity import Entity
from kwai.modules.portal.applications.application import (
    ApplicationEntity,
    ApplicationIdentifier,
)
from kwai.modules.portal.applications.application_db_query import ApplicationDbQuery
from kwai.modules.portal.applications.application_query import ApplicationQuery
from kwai.modules.portal.applications.application_repository import (
    ApplicationRepository,
    ApplicationNotFoundException,
)
from kwai.modules.portal.applications.application_tables import (
    ApplicationsTable,
    ApplicationRow,
)


def _create_entity(row):
    return ApplicationsTable(row).create_entity()


class ApplicationDbRepository(ApplicationRepository):
    """An application database repository.

    Attributes:
        _database: the database for this repository.
    """

    def __init__(self, database: Database):
        self._database = database

    def create_query(self) -> ApplicationQuery:
        return ApplicationDbQuery(self._database)

    async def get_by_id(self, id_: ApplicationIdentifier) -> ApplicationEntity:
        query = self.create_query()
        query.filter_by_id(id_)

        if row := await query.fetch_one():
            return _create_entity(row)

        raise ApplicationNotFoundException(f"Application with {id} does not exist.")

    async def get_by_name(self, name: str) -> ApplicationEntity:
        query = self.create_query()
        query.filter_by_name(name)

        if row := await query.fetch_one():
            return _create_entity(row)

        raise ApplicationNotFoundException(f"Application with {name} does not exist.")

    async def get_all(
        self,
        query: ApplicationQuery,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncIterator[ApplicationEntity]:
        async for row in query.fetch(limit, offset):
            yield _create_entity(row)

    async def create(self, application: ApplicationEntity) -> ApplicationEntity:
        new_id = await self._database.insert(
            ApplicationsTable.table_name, ApplicationRow.persist(application)
        )
        await self._database.commit()
        return Entity.replace(application, id_=ApplicationIdentifier(new_id))

    async def update(self, application: ApplicationEntity) -> None:
        await self._database.update(
            application.id.value,
            ApplicationsTable.table_name,
            ApplicationRow.persist(application),
        )
        await self._database.commit()

    async def delete(self, application: ApplicationEntity) -> None:
        await self._database.delete(application.id.value, ApplicationsTable.table_name)
        await self._database.commit()
