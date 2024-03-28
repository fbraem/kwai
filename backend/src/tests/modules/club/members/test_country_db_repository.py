"""Module for testing the country db repository."""

from typing import AsyncGenerator

import pytest

from kwai.core.db.database import Database
from kwai.modules.club.members.country import CountryEntity
from kwai.modules.club.members.country_db_repository import CountryDbRepository
from kwai.modules.club.members.country_repository import (
    CountryNotFoundException,
    CountryRepository,
)


@pytest.fixture
async def country_repo(database: Database) -> CountryRepository:
    """A fixture for a country repository."""
    return CountryDbRepository(database)


@pytest.fixture(scope="function")
async def country(
    country_repo: CountryRepository, make_country
) -> AsyncGenerator[CountryEntity, None]:
    """A fixture for a country in the database."""
    country = await country_repo.create(
        make_country(iso_2="XX", iso_3="XXX", name="Test")
    )
    yield country
    await country_repo.delete(country)


async def test_create_country(country):
    """Test creating a country."""
    assert country, "Country should be created"


async def test_get_country_by_iso_2(
    country_repo: CountryRepository, country: CountryEntity
):
    """Testing getting a country with an iso_2 code."""
    country = await country_repo.get_by_iso_2("XX")
    assert country.iso_2 == "XX", "The returned country should have iso_2 XX."


async def test_delete_country(country_repo: CountryRepository, country: CountryEntity):
    """Test deleting a country with an iso_2 code."""
    await country_repo.delete(country)
    with pytest.raises(CountryNotFoundException):
        await country_repo.get_by_iso_2("XX")
