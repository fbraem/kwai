"""Module that implements a country repository with a database."""

from sql_smith.query import SelectQuery

from kwai.core.db.database import Database
from kwai.modules.club.members.country_repository import CountryRepository
from kwai.modules.club.members.member_tables import CountryRow
from kwai.modules.club.members.value_objects import Country


class CountryDbRepository(CountryRepository):
    """A repository for countries in a database."""

    def __init__(self, database: Database):
        self._database = database

    async def get_by_iso_2(self, iso_2: str) -> Country | None:
        query: SelectQuery = Database.create_query_factory().select()
        query.from_(CountryRow.__table_name__).columns(*CountryRow.get_aliases()).where(
            CountryRow.field("iso_2").eq(iso_2)
        )
        row = await self._database.fetch_one(query)
        if row:
            return CountryRow.map(row).create_country()

        return None
