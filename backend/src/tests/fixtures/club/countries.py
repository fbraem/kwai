"""Module for fixtures related to countries."""

import pytest
from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.modules.club.domain.country import CountryEntity
from kwai.modules.club.repositories.country_db_repository import CountryDbRepository
from kwai.modules.club.repositories.country_repository import CountryNotFoundException


@pytest.fixture
def make_country():
    """A factory fixture for a country."""

    def _make_country(iso_2="XX", iso_3="XXX", name="Test Country"):
        return CountryEntity(iso_2=iso_2, iso_3=iso_3, name=name)

    return _make_country


@pytest.fixture
def country_japan():
    """A factory fixture for the country Japan."""
    return CountryEntity(iso_2="JP", iso_3="JPN", name="Japan")


@pytest.fixture
async def make_country_in_db(request, event_loop, database: Database, make_country):
    """A fixture for a country in the database.

    When the country is already in the database, it will be returned.
    If not it will be saved in the database, returned and deleted afterward.
    """

    async def _make_country_in_db(
        country: CountryEntity | None = None,
    ) -> CountryEntity:
        country = country or make_country()
        repo = CountryDbRepository(database)
        try:
            country = await repo.get_by_iso_2(country.iso_2)
            return country
        except CountryNotFoundException:
            async with UnitOfWork(database):
                country = await repo.create(country)

            def cleanup():
                async def acleanup():
                    async with UnitOfWork(database):
                        await repo.delete(country)

                event_loop.run_until_complete(acleanup())

            request.addfinalizer(cleanup)

            return country

    return _make_country_in_db
