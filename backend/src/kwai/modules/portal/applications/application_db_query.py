"""Module that implements an ApplicationQuery for a database."""

from kwai.core.db.database_query import DatabaseQuery
from kwai.modules.portal.applications.application import ApplicationIdentifier
from kwai.modules.portal.applications.application_query import ApplicationQuery
from kwai.modules.portal.applications.application_tables import ApplicationsTable


class ApplicationDbQuery(ApplicationQuery, DatabaseQuery):
    """A database query for an application."""

    def init(self):
        return self._query.from_(ApplicationsTable.table_name)

    @property
    def columns(self):
        return ApplicationsTable.aliases()

    def filter_by_id(self, id_: ApplicationIdentifier) -> "ApplicationQuery":
        self._query.and_where(ApplicationsTable.field("id").eq(id_.value))
        return self

    def filter_by_name(self, name: str) -> "ApplicationQuery":
        self._query.and_where(ApplicationsTable.field("name").eq(name))
        return self

    def filter_only_news(self) -> "ApplicationQuery":
        self._query.and_where(ApplicationsTable.field("news").eq(True))
        return self

    def filter_only_pages(self) -> "ApplicationQuery":
        self._query.and_where(ApplicationsTable.field("pages").eq(True))
        return self

    def filter_only_events(self) -> "ApplicationQuery":
        self._query.and_where(ApplicationsTable.field("events").eq(True))
        return self
