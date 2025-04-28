"""Module for defining reusable fixtures."""

from typing import Any

import pytest  # noqa

from kwai.modules.club.domain.country import CountryEntity, CountryIdentifier
from tests.fixtures.identity.users import *  # noqa
from tests.fixtures.portal.authors import *  # noqa


@pytest.fixture
def country() -> CountryEntity:
    """A fixture for a country."""
    return CountryEntity(
        id_=CountryIdentifier(1), iso_2="JP", iso_3="JPN", name="Japan"
    )


@pytest.fixture
def expected_country_json() -> dict[str, Any]:
    """A fixture for a JSON:API resource of a country."""
    return {
        "data": {
            "id": "1",
            "type": "countries",
            "attributes": {"iso_2": "JP", "iso_3": "JPN", "name": "Japan"},
        }
    }
