"""Module that defines a database query for teams."""

from kwai.core.db.database_query import DatabaseQuery
from kwai.modules.training.teams.team import TeamIdentifier
from kwai.modules.training.teams.team_query import TeamQuery
from kwai.modules.training.teams.team_tables import TeamsTable


class TeamDbQuery(DatabaseQuery, TeamQuery):
    """A database query for teams."""

    def init(self):
        self._query.from_(TeamsTable.table_name)

    @property
    def columns(self):
        return TeamsTable.aliases()

    def filter_by_ids(self, *ids: TeamIdentifier) -> "TeamQuery":
        unpacked_ids = tuple(i.value for i in ids)
        self._query.and_where(TeamsTable.field("id").in_(*unpacked_ids))
        return self

    def filter_by_id(self, id_: TeamIdentifier) -> "TeamQuery":
        self._query.and_where(TeamsTable.field("id").eq(id_.value))
        return self
