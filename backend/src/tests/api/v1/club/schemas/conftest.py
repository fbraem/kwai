"""Module for defining reusable fixtures."""

from typing import Any

import pytest
from kwai.core.domain.value_objects.date import Date
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.modules.club.domain.contact import ContactEntity, ContactIdentifier
from kwai.modules.club.domain.country import CountryEntity, CountryIdentifier
from kwai.modules.club.domain.person import PersonEntity, PersonIdentifier
from kwai.modules.club.members.value_objects import Address, Birthdate, Gender


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


@pytest.fixture
def contact(country: CountryEntity) -> ContactEntity:
    """A fixture for a contact entity."""
    return ContactEntity(
        id_=ContactIdentifier(1),
        emails=[EmailAddress("jigoro.kano@kwai.com")],
        address=Address(
            address="",
            postal_code="",
            city="Tokyo",
            county="",
            country=country,
        ),
    )


@pytest.fixture
def expected_contact_json(
    contact: ContactEntity, expected_country_json: dict[str, Any]
) -> dict[str, Any]:
    """A fixture for a JSON:API resource of a contact."""
    return {
        "data": {
            "id": "1",
            "type": "contacts",
            "attributes": {
                "emails": ["jigoro.kano@kwai.com"],
                "address": "",
                "postal_code": "",
                "city": "Tokyo",
                "county": "",
                "mobile": "",
                "tel": "",
                "remark": "",
            },
            "meta": {
                "created_at": str(contact.traceable_time.created_at),
                "updated_at": str(contact.traceable_time.updated_at),
            },
            "relationships": {
                "country": {
                    "data": {
                        "id": expected_country_json["data"]["id"],
                        "type": expected_country_json["data"]["type"],
                    }
                }
            },
        },
        "included": [
            expected_country_json["data"],
        ],
    }


@pytest.fixture
def person(contact: ContactEntity, country: CountryEntity) -> PersonEntity:
    """A fixture for a person entity."""
    return PersonEntity(
        id_=PersonIdentifier(1),
        name=Name(first_name="Jigoro", last_name="Kano"),
        gender=Gender.MALE,
        birthdate=Birthdate(Date.create(year=1860, month=10, day=28)),
        contact=contact,
        nationality=country,
    )


@pytest.fixture
def expected_person_json(
    person: PersonEntity,
    expected_contact_json: dict[str, Any],
    expected_country_json: dict[str, Any],
) -> dict[str, Any]:
    """A fixture for a JSON:API resource of a person."""
    return {
        "data": {
            "id": "1",
            "type": "persons",
            "attributes": {
                "first_name": "Jigoro",
                "last_name": "Kano",
                "gender": 1,
                "birthdate": "1860-10-28",
                "remark": "",
            },
            "meta": {
                "created_at": str(person.traceable_time.created_at),
                "updated_at": str(person.traceable_time.updated_at),
            },
            "relationships": {
                "nationality": {
                    "data": {
                        "id": expected_country_json["data"]["id"],
                        "type": expected_country_json["data"]["type"],
                    }
                },
                "contact": {
                    "data": {
                        "id": expected_contact_json["data"]["id"],
                        "type": expected_contact_json["data"]["type"],
                    }
                },
            },
        },
        "included": [expected_contact_json["data"], expected_country_json["data"]],
    }
