"""Module for defining a coach repository using a database."""

from kwai.core.db.database import Database
from kwai.core.domain.entity import Entity
from kwai.modules.club.domain.coach import CoachEntity, CoachIdentifier
from kwai.modules.club.repositories._tables import CoachRow
from kwai.modules.club.repositories.coach_repository import CoachRepository


class CoachDbRepository(CoachRepository):
    """A coach repository using a database."""

    def __init__(self, database: Database) -> None:
        self._database = database

    async def create(self, coach: CoachEntity):
        new_coach_id = await self._database.insert(
            CoachRow.__table_name__, CoachRow.persist(coach)
        )
        return Entity.replace(coach, id_=CoachIdentifier(new_coach_id))

    async def delete(self, coach: CoachEntity):
        await self._database.delete(coach.id.value, CoachRow.__table_name__)
