"""Module for testing the country db repository."""
from kwai.core.db.database import Database
from kwai.modules.club.members.country_db_repository import CountryDbRepository


async def test_get_iso_2(database: Database):
    """Testing getting a country with an iso_2 code."""
    country = await CountryDbRepository(database).get_by_iso_2("BE")
    assert country.iso_2 == "BE", "The returned country should have iso_2 BE."
