"""Module that implements a team repository for a database."""

from kwai.core.db.database import Database
from kwai.core.domain.entity import Entity
from kwai.modules.club.domain.team import TeamEntity, TeamIdentifier
from kwai.modules.club.repositories._tables import TeamRow
from kwai.modules.club.repositories.team_repository import TeamRepository


class TeamDbRepository(TeamRepository):
    """A team repository for a database."""

    def __init__(self, database: Database):
        self._database = database

    async def create(self, team: TeamEntity) -> TeamEntity:
        new_team_id = await self._database.insert(
            TeamRow.__table_name__, TeamRow.persist(team)
        )
        return Entity.replace(team, id_=TeamIdentifier(new_team_id))

    async def delete(self, team: TeamEntity) -> None:
        await self._database.delete(team.id.value, TeamRow.__table_name__)
