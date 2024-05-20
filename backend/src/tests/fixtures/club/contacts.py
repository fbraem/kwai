"""Module for defining fixtures for contacts."""

from typing import (
    Awaitable,
    Callable,
    NotRequired,
    TypeAlias,
    TypedDict,
    Unpack,
)

import pytest
from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.modules.club.domain.contact import ContactEntity
from kwai.modules.club.domain.country import CountryEntity
from kwai.modules.club.domain.value_objects import Address
from kwai.modules.club.repositories.contact_db_repository import ContactDbRepository


class AddressType(TypedDict):
    """Keyword arguments for the Address fixture factory method."""

    address: NotRequired[str]
    postal_code: NotRequired[str]
    city: NotRequired[str]
    county: NotRequired[str]
    country: NotRequired[CountryEntity]


AddressFixtureFactory: TypeAlias = Callable[[Unpack[AddressType]], Address]


@pytest.fixture
def make_address(country_japan) -> AddressFixtureFactory:
    """A factory fixture for an address."""

    def _make_address(
        *,
        address: str = "1-16-30 Kasuga",
        postal_code: str = "112-0003",
        city: str = "Tokyo",
        county: str = "Bunkyo-ku",
        country: CountryEntity | None = None,
    ) -> Address:
        return Address(
            address=address,
            postal_code=postal_code,
            city=city,
            county=county,
            country=country or country_japan,
        )

    return _make_address


class ContactType(TypedDict):
    """Keyword arguments for the Contact fixture factory method."""

    emails: NotRequired[list[EmailAddress]]
    address: NotRequired[Address]


ContactFixtureFactory: TypeAlias = Callable[[Unpack[ContactType]], ContactEntity]


@pytest.fixture
def make_emails() -> Callable[[str | None], list[EmailAddress]]:
    """A factory fixture for a contact email."""

    def _make_emails(email: str | None = None) -> list[EmailAddress]:
        if email is None:
            return [EmailAddress("jigoro.kano@kwai.com")]
        return [EmailAddress(email)]

    return _make_emails


@pytest.fixture
def make_contact(make_emails, make_address) -> ContactFixtureFactory:
    """A factory fixture for a contact."""

    def _make_contact(
        *, emails: list[EmailAddress] | None = None, address: Address | None = None
    ):
        return ContactEntity(
            emails=emails or make_emails(),
            address=address or make_address(),
        )

    return _make_contact


ContactDbFixtureFactory: TypeAlias = Callable[
    [ContactEntity | None], Awaitable[ContactEntity]
]


@pytest.fixture
def make_contact_in_db(
    request,
    event_loop,
    database: Database,
    make_contact,
    make_address,
    make_country_in_db,
) -> ContactDbFixtureFactory:
    """A fixture for a contact in the database."""

    async def _make_contact_in_db(
        contact: ContactEntity | None = None,
    ) -> ContactEntity:
        contact = contact or make_contact(
            address=make_address(country=await make_country_in_db())
        )
        repo = ContactDbRepository(database)
        async with UnitOfWork(database):
            contact = await repo.create(contact)

        def cleanup():
            async def acleanup():
                async with UnitOfWork(database):
                    await repo.delete(contact)

            event_loop.run_until_complete(acleanup())

        request.addfinalizer(cleanup)

        return contact

    return _make_contact_in_db
