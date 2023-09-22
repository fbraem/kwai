"""Module that implements a page repository for a database."""
from typing import Any, AsyncIterator

from sql_smith.functions import field

from kwai.core.db.database import Database
from kwai.core.db.rows import OwnersTable
from kwai.core.domain.entity import Entity
from kwai.core.functions import async_groupby
from kwai.modules.portal.applications.application_tables import ApplicationsTable
from kwai.modules.portal.pages.page import PageEntity, PageIdentifier
from kwai.modules.portal.pages.page_db_query import PageDbQuery
from kwai.modules.portal.pages.page_query import PageQuery
from kwai.modules.portal.pages.page_repository import (
    PageNotFoundException,
    PageRepository,
)
from kwai.modules.portal.pages.page_tables import (
    PageContentRow,
    PageContentsTable,
    PageRow,
    PagesTable,
)


def _create_entity(rows: list[dict[str, Any]]) -> PageEntity:
    """Create a story entity from a group of rows."""
    return PagesTable(rows[0]).create_entity(
        ApplicationsTable(rows[0]).create_entity(),
        [
            PageContentsTable(row).create_content(
                author=OwnersTable(row).create_owner()
            )
            for row in rows
        ],
    )


class PageDbRepository(PageRepository):
    """Page repository for a database."""

    def __init__(self, database: Database):
        self._database = database

    async def create(self, page: PageEntity) -> PageEntity:
        new_id = await self._database.insert(
            PagesTable.table_name, PageRow.persist(page)
        )
        result = Entity.replace(page, id_=PageIdentifier(new_id))

        content_rows = [
            PageContentRow.persist(result, content) for content in page.texts
        ]
        await self._database.insert(PageContentsTable.table_name, *content_rows)

        await self._database.commit()
        return result

    async def update(self, page: PageEntity):
        await self._database.update(
            page.id.value, PagesTable.table_name, PageRow.persist(page)
        )

        delete_contents_query = (
            self._database.create_query_factory()
            .delete(PageContentsTable.table_name)
            .where(field("page_id").eq(page.id.value))
        )
        await self._database.execute(delete_contents_query)

        content_rows = [PageContentRow.persist(page, content) for content in page.texts]
        await self._database.insert(PageContentsTable.table_name, *content_rows)
        await self._database.commit()

    async def delete(self, page: PageEntity):
        delete_contents_query = (
            self._database.create_query_factory()
            .delete(PageContentsTable.table_name)
            .where(field("page_id").eq(page.id.value))
        )
        await self._database.execute(delete_contents_query)
        await self._database.delete(page.id.value, PagesTable.table_name)
        await self._database.commit()

    def create_query(self) -> PageQuery:
        return PageDbQuery(self._database)

    async def get_by_id(self, id_: PageIdentifier) -> PageEntity:
        query = self.create_query()
        query.filter_by_id(id_)

        entity = await anext(self.get_all(query, 1), None)
        if entity is None:
            raise PageNotFoundException(f"Page with {id} does not exist.")

        return entity

    async def get_all(
        self,
        query: PageQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncIterator[PageEntity]:
        if query is None:
            query = self.create_query()

        group_by_column = PagesTable.alias_name("id")

        row_iterator = query.fetch(limit, offset)
        async for _, group in async_groupby(
            row_iterator, key=lambda row: row[group_by_column]
        ):
            yield _create_entity(group)
