"""Module that implements a news item repository for a database."""
from typing import Any, AsyncIterator

from sql_smith.functions import field

from kwai.core.db.database import Database
from kwai.core.db.rows import OwnersTable
from kwai.core.domain.entity import Entity
from kwai.modules.portal.applications.application_tables import ApplicationsTable
from kwai.modules.portal.news.news_item import NewsItemEntity, NewsItemIdentifier
from kwai.modules.portal.news.news_item_db_query import NewsItemDbQuery
from kwai.modules.portal.news.news_item_query import NewsItemQuery
from kwai.modules.portal.news.news_item_repository import (
    NewsItemNotFoundException,
    NewsItemRepository,
)
from kwai.modules.portal.news.news_tables import (
    NewsItemRow,
    NewsItemsTable,
    NewsItemTextRow,
    NewsItemTextsTable,
)


def _create_entity(rows: list[dict[str, Any]]) -> NewsItemEntity:
    """Create a news item entity from a group of rows."""
    return NewsItemsTable(rows[0]).create_entity(
        ApplicationsTable(rows[0]).create_entity(),
        [
            NewsItemTextsTable(row).create_content(
                author=OwnersTable(row).create_owner()
            )
            for row in rows
        ],
    )


class NewsItemDbRepository(NewsItemRepository):
    """A news item database repository.

    Attributes:
        _database: the database for the repository.
    """

    def __init__(self, database: Database):
        self._database = database

    async def create(self, news_item: NewsItemEntity) -> NewsItemEntity:
        new_id = await self._database.insert(
            NewsItemsTable.table_name, NewsItemRow.persist(news_item)
        )
        result = Entity.replace(news_item, id_=NewsItemIdentifier(new_id))

        content_rows = [
            NewsItemTextRow.persist(result, content) for content in news_item.texts
        ]
        await self._database.insert(NewsItemTextsTable.table_name, *content_rows)

        await self._database.commit()
        return result

    async def update(self, news_item: NewsItemEntity):
        await self._database.update(
            news_item.id.value,
            NewsItemsTable.table_name,
            NewsItemRow.persist(news_item),
        )

        delete_contents_query = (
            self._database.create_query_factory()
            .delete(NewsItemTextsTable.table_name)
            .where(field("news_id").eq(news_item.id.value))
        )
        await self._database.execute(delete_contents_query)

        content_rows = [
            NewsItemTextRow.persist(news_item, content) for content in news_item.texts
        ]
        await self._database.insert(NewsItemTextsTable.table_name, *content_rows)
        await self._database.commit()

    async def delete(self, news_item: NewsItemEntity):
        delete_contents_query = (
            self._database.create_query_factory()
            .delete(NewsItemTextsTable.table_name)
            .where(field("news_id").eq(news_item.id.value))
        )
        await self._database.execute(delete_contents_query)
        await self._database.delete(news_item.id.value, NewsItemsTable.table_name)
        await self._database.commit()

    def create_query(self) -> NewsItemQuery:
        return NewsItemDbQuery(self._database)

    async def get_by_id(self, id_: NewsItemIdentifier) -> NewsItemEntity:
        query = self.create_query()
        query.filter_by_id(id_)

        entity = await anext(self.get_all(query, 1), None)
        if entity is None:
            raise NewsItemNotFoundException(f"News item with {id} does not exist.")

        return entity

    async def get_all(
        self,
        query: NewsItemQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncIterator[NewsItemEntity]:
        if query is None:
            query = self.create_query()

        group_by_column = NewsItemsTable.alias_name("id")

        row_it = query.fetch(limit, offset)

        # Handle the first row
        try:
            row = await anext(row_it)
        except StopAsyncIteration:
            return

        group = [row]
        current_key = row[group_by_column]

        # Process all other rows
        async for row in row_it:
            new_key = row[group_by_column]
            if new_key != current_key:
                yield _create_entity(group)
                group = [row]
                current_key = new_key
            else:
                group.append(row)

        yield _create_entity(group)
