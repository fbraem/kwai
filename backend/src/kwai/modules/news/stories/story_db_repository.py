"""Module that implements a story repository for a database."""
from typing import AsyncIterator, Any

from sql_smith.functions import field

from kwai.core.db.database import Database
from kwai.core.domain.entity import Entity
from kwai.modules.news.stories.story import StoryEntity, StoryIdentifier
from kwai.modules.news.stories.story_db_query import StoryDbQuery
from kwai.modules.news.stories.story_query import StoryQuery
from kwai.modules.news.stories.story_repository import (
    StoryRepository,
    StoryNotFoundException,
)
from kwai.modules.news.stories.story_tables import (
    StoriesTable,
    ApplicationsTable,
    StoryContentsTable,
    StoryRow,
    StoryContentRow,
    AuthorsTable,
)


def _create_entity(rows: list[dict[str, Any]]) -> StoryEntity:
    """Create a story entity from a group of rows."""
    return StoriesTable(rows[0]).create_entity(
        ApplicationsTable(rows[0]).create_application(),
        [
            StoryContentsTable(row).create_content(
                author=AuthorsTable(row).create_author()
            )
            for row in rows
        ],
    )


class StoryDbRepository(StoryRepository):
    """A story database repository.

    Attributes:
        _database: the database for the repository.
    """

    def __init__(self, database: Database):
        self._database = database

    async def create(self, story: StoryEntity) -> StoryEntity:
        new_id = await self._database.insert(
            StoriesTable.table_name, StoryRow.persist(story)
        )
        result = Entity.replace(story, id_=StoryIdentifier(new_id))

        content_rows = [
            StoryContentRow.persist(result, content) for content in story.content
        ]
        await self._database.insert(StoryContentsTable.table_name, *content_rows)

        await self._database.commit()
        return result

    async def update(self, story: StoryEntity):
        await self._database.update(
            story.id.value, StoriesTable.table_name, StoryRow.persist(story)
        )
        await self._database.create_query_factory().delete(
            StoryContentsTable.table_name
        ).where(field("news_id").eq(story.id.value))
        content_rows = [
            StoryContentRow.persist(story, content) for content in story.content
        ]
        await self._database.insert(StoryContentsTable.table_name, *content_rows)
        await self._database.commit()

    async def delete(self, story: StoryEntity):
        delete_contents_query = (
            self._database.create_query_factory()
            .delete(StoryContentsTable.table_name)
            .where(field("news_id").eq(story.id.value))
        )
        await self._database.execute(delete_contents_query)
        await self._database.delete(story.id.value, StoriesTable.table_name)
        await self._database.commit()

    def create_query(self) -> StoryQuery:
        return StoryDbQuery(self._database)

    async def get_by_id(self, id_: StoryIdentifier) -> StoryEntity:
        query = self.create_query()
        query.filter_by_id(id_)

        entity = await anext(self.get_all(query, 1), None)
        if entity is None:
            raise StoryNotFoundException(f"Story with {id} does not exist.")

        return entity

    async def get_all(
        self,
        query: StoryQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncIterator[StoryEntity]:
        if query is None:
            query = self.create_query()

        group_by_column = StoriesTable.alias_name("id")

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
