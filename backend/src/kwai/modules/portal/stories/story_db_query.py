"""Module that implements a StoryQuery for a database."""
from datetime import datetime
from typing import AsyncIterator

from sql_smith.functions import criteria, express, func, group, literal, on

from kwai.core.db.database import Database
from kwai.core.db.database_query import DatabaseQuery
from kwai.core.db.rows import OwnersTable
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.portal.stories.story import StoryIdentifier
from kwai.modules.portal.stories.story_query import StoryQuery
from kwai.modules.portal.stories.story_tables import (
    ApplicationsTable,
    StoriesTable,
    StoryContentsTable,
)


class StoryDbQuery(StoryQuery, DatabaseQuery):
    """A database query for news stories."""

    def __init__(self, database: Database):
        self._main_query = database.create_query_factory().select()
        super().__init__(database)

    def init(self):
        # This query will be used as CTE, so only join the tables that are needed
        # for counting and limiting the results.
        self._query.from_(StoriesTable.table_name).join(
            ApplicationsTable.table_name,
            on(
                ApplicationsTable.column("id"),
                StoriesTable.column("application_id"),
            ),
        )

        self._main_query = (
            self._main_query.from_(StoriesTable.table_name)
            .columns(*(self.columns + StoryContentsTable.aliases()))
            .with_("limited", self._query)
            .right_join("limited", on("limited.id", StoriesTable.column("id")))
            .join(
                ApplicationsTable.table_name,
                on(
                    ApplicationsTable.column("id"),
                    StoriesTable.column("application_id"),
                ),
            )
            .join(
                StoryContentsTable.table_name,
                on(StoryContentsTable.column("news_id"), StoriesTable.column("id")),
            )
            .join(
                OwnersTable.table_name,
                on(OwnersTable.column("id"), StoryContentsTable.column("user_id")),
            )
        )

    @property
    def columns(self):
        return (
            StoriesTable.aliases() + ApplicationsTable.aliases() + OwnersTable.aliases()
        )

    @property
    def count_column(self) -> str:
        return StoriesTable.column("id")

    def filter_by_id(self, id_: StoryIdentifier) -> "StoryQuery":
        self._query.and_where(StoriesTable.field("id").eq(id_.value))
        return self

    def filter_by_publication_date(
        self, year: int, month: int | None = None
    ) -> "StoryQuery":
        condition = criteria(
            "{} = {}", func("YEAR", StoriesTable.column("publish_date")), literal(year)
        )
        if month is not None:
            condition.and_(
                criteria(
                    "{} = {}",
                    func("MONTH", StoriesTable.column("publish_date")),
                    literal(month),
                )
            )
        self._query.and_where(condition)
        return self

    def filter_by_promoted(self) -> "StoryQuery":
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        condition = (
            StoriesTable.field("promotion")
            .gt(0)
            .and_(
                group(
                    StoriesTable.field("promotion_end_date")
                    .is_null()
                    .or_(StoriesTable.field("promotion_end_date").gt(now))
                )
            )
        )
        self._query.and_where(condition)
        self._query.order_by(StoriesTable.column("promotion"))
        return self

    def filter_by_application(self, application: int | str) -> "StoryQuery":
        if isinstance(application, str):
            self._query.and_where(ApplicationsTable.field("name").eq(application))
        else:
            self._query.and_where(ApplicationsTable.field("id").eq(application))

        return self

    def filter_by_active(self) -> "StoryQuery":
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        self._query.and_where(
            group(
                StoriesTable.field("enabled")
                .eq(True)
                .and_(StoriesTable.field("publish_date").lte(now))
                .or_(
                    group(
                        StoriesTable.field("end_date")
                        .is_not_null()
                        .and_(StoriesTable.field("end_date").gt(now))
                    )
                )
            )
        )

        return self

    def filter_by_user(self, user: int | UniqueId) -> "StoryQuery":
        inner_select = (
            self._database.create_query_factory()
            .select(OwnersTable.column("id"))
            .from_(OwnersTable.table_name)
        )
        if isinstance(user, UniqueId):
            inner_select.where(OwnersTable.field("uuid").eq(str(user)))
        else:
            inner_select.where(OwnersTable.field("id").eq(user))

        self._main_query.and_where(
            group(StoryContentsTable.field("user_id").in_(express("%s", inner_select)))
        )
        return self

    def order_by_publication_date(self) -> "StoryQuery":
        self._main_query.order_by(StoriesTable.column("publish_date"), "DESC")
        # Also add the order to the CTE
        self._query.order_by(StoriesTable.column("publish_date"), "DESC")
        return self

    def fetch(
        self, limit: int | None = None, offset: int | None = None
    ) -> AsyncIterator[dict[str, any]]:
        self._query.limit(limit)
        self._query.offset(offset)
        self._query.columns(StoriesTable.column("id"))
        self._main_query.order_by(StoriesTable.column("id"))

        return self._database.fetch(self._main_query)
