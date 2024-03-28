"""Module that defines tests for the ContactEntity."""

import pytest

from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.modules.club.members.contact import ContactEntity
from kwai.modules.club.members.country import CountryEntity, CountryIdentifier
from kwai.modules.club.members.value_objects import Address


@pytest.fixture
def country() -> CountryEntity:
    """A fixture for a country."""
    return CountryEntity(
        id_=CountryIdentifier(1), iso_2="BE", iso_3="BEL", name="Belgium"
    )


def test_add_email(country: CountryEntity):
    """Test adding an email address."""
    contact = ContactEntity(
        address=Address(
            address="",
            postal_code="",
            city="",
            county="",
            country=country,
        )
    )
    contact.add_email(EmailAddress("jigoro.kano@kwai.com"))
    assert len(contact.emails) == 1, "There should be 1 email address."


def test_remove_email(country: CountryEntity):
    """Test adding an email address."""
    contact = ContactEntity(
        address=Address(
            address="",
            postal_code="",
            city="",
            county="",
            country=country,
        )
    )
    contact.add_email(EmailAddress("jigoro.kano@kwai.com"))
    contact.add_email(EmailAddress("jigoro.kano2@kwai.com"))
    assert len(contact.emails) == 2, "There should be 2 email addresses."
    contact.remove_email(EmailAddress("jigoro.kano@kwai.com"))
    assert len(contact.emails) == 1, "There should be 1 email address."
    assert contact.emails[0] == EmailAddress("jigoro.kano2@kwai.com")
