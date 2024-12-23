"""Module for defining an importer for members of the Flemish Judo Federation."""

import csv
from typing import Any, AsyncGenerator

from kwai.core.domain.value_objects.date import Date
from kwai.core.domain.value_objects.email_address import (
    EmailAddress,
    InvalidEmailException,
)
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.owner import Owner
from kwai.modules.club.domain.contact import ContactEntity
from kwai.modules.club.domain.member import MemberEntity
from kwai.modules.club.domain.person import PersonEntity
from kwai.modules.club.domain.value_objects import Address, Birthdate, Gender, License
from kwai.modules.club.repositories.country_repository import (
    CountryNotFoundException,
    CountryRepository,
)
from kwai.modules.club.repositories.member_importer import (
    FailureResult,
    MemberImporter,
    OkResult,
    Result,
)


class FlemishMemberImporter(MemberImporter):
    """A class for importing members of the Flemish Judo Federation.

    The import is a csv file.
    """

    def __init__(self, filename: str, owner: Owner, country_repo: CountryRepository):
        """Initialize the importer.

        Args:
            filename: The name of the csv file.
            owner: The user that started the upload.
            country_repo: A repository to get the nationality of a member.
        """
        super().__init__(filename, owner, country_repo)

    async def import_(self) -> AsyncGenerator[Result, None]:
        with open(self._filename) as csv_file:
            member_reader = csv.DictReader(csv_file)
            row: dict[str, Any]
            for row_index, row in enumerate(member_reader):
                if row["geslacht"] == "V":
                    gender = Gender.FEMALE
                elif row["geslacht"] == "M":
                    gender = Gender.MALE
                else:
                    gender = Gender.UNKNOWN

                try:
                    nationality = await self._get_country(
                        self._country_repo, row["nationaliteit"]
                    )
                except CountryNotFoundException:
                    yield FailureResult(
                        row=row_index,
                        message=f"Unrecognized country: {row['nationaliteit']}",
                    )
                    continue

                emails = []
                try:
                    for email in row["email"].split(";"):
                        emails.append(EmailAddress(email.strip()))
                except InvalidEmailException as exc:
                    yield FailureResult(row=row_index, message=str(exc))
                    continue

                try:
                    country = await self._get_country(self._country_repo, row["land"])
                except CountryNotFoundException:
                    yield FailureResult(
                        row=row_index,
                        message=f"Unrecognized country: {row['land']}",
                    )
                    continue

                yield OkResult(
                    row=row_index,
                    member=MemberEntity(
                        license=License(
                            number=row["vergunning"],
                            end_date=Date.create_from_string(row["vervaldatum"]),
                        ),
                        person=PersonEntity(
                            name=Name(
                                first_name=row["voornaam"], last_name=row["achternaam"]
                            ),
                            gender=gender,
                            birthdate=Birthdate(
                                Date.create_from_string(row["geboortedatum"])
                            ),
                            nationality=nationality,
                            contact=ContactEntity(
                                emails=emails,
                                address=Address(
                                    address=row["straatnummer"],
                                    postal_code=row["postnummer"],
                                    city=row["gemeente"],
                                    county="",
                                    country=country,
                                ),
                                mobile=row["telefoon1"],
                                tel=row["telefoon2"],
                            ),
                        ),
                        active=row["status"] == "ACTIEF",
                    ),
                )
        self._get_country.cache_clear()
