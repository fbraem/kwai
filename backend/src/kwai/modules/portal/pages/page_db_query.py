"""Module that implements a PageQuery for a database."""
from typing import AsyncIterator

from sql_smith.functions import express, group, on

from kwai.core.db.database import Database
from kwai.core.db.database_query import DatabaseQuery
from kwai.core.db.rows import OwnersTable
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.portal.pages.page import PageIdentifier
from kwai.modules.portal.pages.page_query import PageQuery
from kwai.modules.portal.pages.page_tables import (
    ApplicationsTable,
    PageContentsTable,
    PagesTable,
)


class PageDbQuery(PageQuery, DatabaseQuery):
    """A database query for pages."""

    def __init__(self, database: Database):
        self._main_query = database.create_query_factory().select()
        super().__init__(database)

    def init(self):
        self._query.from_(PagesTable.table_name).join(
            ApplicationsTable.table_name,
            on(
                ApplicationsTable.column("id"),
                PagesTable.column("application_id"),
            ),
        )
        self._main_query = (
            self._main_query.from_(PagesTable.table_name)
            .columns(*(self.columns + PageContentsTable.aliases()))
            .with_("limited", self._query)
            .right_join("limited", on("limited.id", PagesTable.column("id")))
            .join(
                ApplicationsTable.table_name,
                on(
                    ApplicationsTable.column("id"),
                    PagesTable.column("application_id"),
                ),
            )
            .join(
                PageContentsTable.table_name,
                on(PageContentsTable.column("page_id"), PagesTable.column("id")),
            )
            .join(
                OwnersTable.table_name,
                on(OwnersTable.column("id"), PageContentsTable.column("user_id")),
            )
        )

    @property
    def columns(self):
        return (
            PagesTable.aliases() + ApplicationsTable.aliases() + OwnersTable.aliases()
        )

    @property
    def count_column(self) -> str:
        return PagesTable.column("id")

    def filter_by_id(self, id_: PageIdentifier) -> "PageQuery":
        self._query.and_where(PagesTable.field("id").eq(id_.value))
        return self

    def filter_by_application(self, application: int | str) -> "PageQuery":
        if isinstance(application, str):
            self._query.and_where(ApplicationsTable.field("name").eq(application))
        else:
            self._query.and_where(ApplicationsTable.field("id").eq(application))
        return self

    def filter_by_active(self) -> "PageQuery":
        self._query.and_where(PagesTable.field("enabled").eq(1))
        return self

    def filter_by_user(self, user: int | UniqueId) -> "PageQuery":
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
            group(PageContentsTable.field("user_id").in_(express("%s", inner_select)))
        )
        return self

    def fetch(
        self, limit: int | None = None, offset: int | None = None
    ) -> AsyncIterator[dict[str, any]]:
        self._query.limit(limit)
        self._query.offset(offset)
        self._query.columns(PagesTable.column("id"))
        self._main_query.order_by(PagesTable.column("priority"))
        self._main_query.order_by(PagesTable.column("id"))

        return self._database.fetch(self._main_query)
