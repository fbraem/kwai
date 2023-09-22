"""Module that implements a NewsItemQuery for a database."""
from datetime import datetime
from typing import AsyncIterator

from sql_smith.functions import criteria, express, func, group, literal, on

from kwai.core.db.database import Database
from kwai.core.db.database_query import DatabaseQuery
from kwai.core.db.rows import OwnersTable
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.portal.applications.application_tables import ApplicationsTable
from kwai.modules.portal.news.news_item import NewsItemIdentifier
from kwai.modules.portal.news.news_item_query import NewsItemQuery
from kwai.modules.portal.news.news_tables import (
    NewsItemsTable,
    NewsItemTextsTable,
)


class NewsItemDbQuery(NewsItemQuery, DatabaseQuery):
    """A database query for news stories."""

    def __init__(self, database: Database):
        self._main_query = database.create_query_factory().select()
        super().__init__(database)

    def init(self):
        # This query will be used as CTE, so only join the tables that are needed
        # for counting and limiting the results.
        self._query.from_(NewsItemsTable.table_name).join(
            ApplicationsTable.table_name,
            on(
                ApplicationsTable.column("id"),
                NewsItemsTable.column("application_id"),
            ),
        )

        self._main_query = (
            self._main_query.from_(NewsItemsTable.table_name)
            .columns(*(self.columns + NewsItemTextsTable.aliases()))
            .with_("limited", self._query)
            .right_join("limited", on("limited.id", NewsItemsTable.column("id")))
            .join(
                ApplicationsTable.table_name,
                on(
                    ApplicationsTable.column("id"),
                    NewsItemsTable.column("application_id"),
                ),
            )
            .join(
                NewsItemTextsTable.table_name,
                on(NewsItemTextsTable.column("news_id"), NewsItemsTable.column("id")),
            )
            .join(
                OwnersTable.table_name,
                on(OwnersTable.column("id"), NewsItemTextsTable.column("user_id")),
            )
        )

    @property
    def columns(self):
        return (
            NewsItemsTable.aliases()
            + ApplicationsTable.aliases()
            + OwnersTable.aliases()
        )

    @property
    def count_column(self) -> str:
        return NewsItemsTable.column("id")

    def filter_by_id(self, id_: NewsItemIdentifier) -> "NewsItemQuery":
        self._query.and_where(NewsItemsTable.field("id").eq(id_.value))
        return self

    def filter_by_publication_date(
        self, year: int, month: int | None = None
    ) -> "NewsItemQuery":
        condition = criteria(
            "{} = {}",
            func("YEAR", NewsItemsTable.column("publish_date")),
            literal(year),
        )
        if month is not None:
            condition.and_(
                criteria(
                    "{} = {}",
                    func("MONTH", NewsItemsTable.column("publish_date")),
                    literal(month),
                )
            )
        self._query.and_where(condition)
        return self

    def filter_by_promoted(self) -> "NewsItemQuery":
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        condition = (
            NewsItemsTable.field("promotion")
            .gt(0)
            .and_(
                group(
                    NewsItemsTable.field("promotion_end_date")
                    .is_null()
                    .or_(NewsItemsTable.field("promotion_end_date").gt(now))
                )
            )
        )
        self._query.and_where(condition)
        self._query.order_by(NewsItemsTable.column("promotion"))
        return self

    def filter_by_application(self, application: int | str) -> "NewsItemQuery":
        if isinstance(application, str):
            self._query.and_where(ApplicationsTable.field("name").eq(application))
        else:
            self._query.and_where(ApplicationsTable.field("id").eq(application))

        return self

    def filter_by_active(self) -> "NewsItemQuery":
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        self._query.and_where(
            group(
                NewsItemsTable.field("enabled")
                .eq(True)
                .and_(NewsItemsTable.field("publish_date").lte(now))
                .or_(
                    group(
                        NewsItemsTable.field("end_date")
                        .is_not_null()
                        .and_(NewsItemsTable.field("end_date").gt(now))
                    )
                )
            )
        )

        return self

    def filter_by_user(self, user: int | UniqueId) -> "NewsItemQuery":
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
            group(NewsItemTextsTable.field("user_id").in_(express("%s", inner_select)))
        )
        return self

    def order_by_publication_date(self) -> "NewsItemQuery":
        self._main_query.order_by(NewsItemsTable.column("publish_date"), "DESC")
        # Also add the order to the CTE
        self._query.order_by(NewsItemsTable.column("publish_date"), "DESC")
        return self

    def fetch(
        self, limit: int | None = None, offset: int | None = None
    ) -> AsyncIterator[dict[str, any]]:
        self._query.limit(limit)
        self._query.offset(offset)
        self._query.columns(NewsItemsTable.column("id"))
        self._main_query.order_by(NewsItemsTable.column("id"))

        return self._database.fetch(self._main_query)
