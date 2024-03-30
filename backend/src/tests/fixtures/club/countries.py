"""Module for fixtures related to countries."""

from typing import (
    AsyncGenerator,
    Callable,
    NotRequired,
    TypedDict,
    Unpack,
)

import pytest

from kwai.core.db.database import Database
from kwai.modules.club.members.country import CountryEntity
from kwai.modules.club.members.country_db_repository import CountryDbRepository
from kwai.modules.club.members.country_repository import CountryNotFoundException


class CountryType(TypedDict):
    """Keyword arguments for the Country fixture factory method."""

    iso_2: NotRequired[str]
    iso_3: NotRequired[str]
    name: NotRequired[str]


type CountryFixtureFactory = Callable[[Unpack[CountryType]], CountryEntity]


@pytest.fixture
def make_country() -> CountryFixtureFactory:
    """A factory fixture for a country."""

    def _make_country(iso_2="XX", iso_3="XXX", name="Test Country"):
        return CountryEntity(iso_2=iso_2, iso_3=iso_3, name=name)

    return _make_country


type CountryDbFixtureFactory = Callable[[], AsyncGenerator[CountryEntity, None]]


@pytest.fixture
async def make_country_in_db(
    request, event_loop, database: Database, make_country: CountryFixtureFactory
) -> CountryDbFixtureFactory:
    """A fixture for a country in the database.

    When the country is already in the database, it will be yielded.
    If not it will be saved in the database, yielded and deleted afterward.
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
            country = await repo.create(country)

            def cleanup():
                async def acleanup():
                    await repo.delete(country)

                event_loop.run_until_complete(acleanup())

            request.addfinalizer(cleanup)

            return country

    return _make_country_in_db
