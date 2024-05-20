"""Module for testing the country db repository."""

import pytest
from kwai.core.db.database import Database
from kwai.modules.club.domain.country import CountryEntity
from kwai.modules.club.members.country_db_repository import CountryDbRepository
from kwai.modules.club.members.country_repository import (
    CountryNotFoundException,
    CountryRepository,
)

pytestmark = pytest.mark.db


@pytest.fixture
async def country_repo(database: Database) -> CountryRepository:
    """A fixture for a country repository."""
    return CountryDbRepository(database)


async def test_create_country(make_country_in_db):
    """Test creating a country."""
    country = await make_country_in_db(
        CountryEntity(iso_2="XX", iso_3="XXX", name="Test")
    )
    assert not country.id.is_empty(), "Country should be created"


async def test_get_country_by_iso_2(
    country_repo: CountryRepository, make_country_in_db
):
    """Testing getting a country with an iso_2 code."""
    await make_country_in_db(CountryEntity(iso_2="XX", iso_3="XXX", name="Test"))
    country = await country_repo.get_by_iso_2("XX")
    assert country.iso_2 == "XX", "The returned country should have iso_2 XX."


async def test_delete_country(country_repo: CountryRepository, make_country_in_db):
    """Test deleting a country with an iso_2 code."""
    country = await make_country_in_db(
        CountryEntity(iso_2="XX", iso_3="XXX", name="Test")
    )
    await country_repo.delete(country)
    with pytest.raises(CountryNotFoundException):
        await country_repo.get_by_iso_2("XX")
