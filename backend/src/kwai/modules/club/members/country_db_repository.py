"""Module that implements a country repository with a database."""

from sql_smith.query import SelectQuery

from kwai.core.db.database import Database
from kwai.core.domain.entity import Entity
from kwai.modules.club.domain.country import CountryEntity, CountryIdentifier
from kwai.modules.club.members.country_repository import (
    CountryNotFoundException,
    CountryRepository,
)
from kwai.modules.club.members.member_tables import CountryRow


class CountryDbRepository(CountryRepository):
    """A repository for countries in a database."""

    def __init__(self, database: Database):
        self._database = database

    async def get_by_iso_2(self, iso_2: str) -> CountryEntity:
        query: SelectQuery = Database.create_query_factory().select()
        query.from_(CountryRow.__table_name__).columns(*CountryRow.get_aliases()).where(
            CountryRow.field("iso_2").eq(iso_2)
        )
        row = await self._database.fetch_one(query)
        if row:
            return CountryRow.map(row).create_country()

        raise CountryNotFoundException(f"Country with iso 2 {iso_2} does not exist.")

    async def create(self, country: CountryEntity) -> CountryEntity:
        new_id = await self._database.insert(
            CountryRow.__table_name__, CountryRow.persist(country)
        )
        return Entity.replace(country, id_=CountryIdentifier(new_id))

    async def delete(self, country: CountryEntity):
        await self._database.delete(country.id.value, CountryRow.__table_name__)
