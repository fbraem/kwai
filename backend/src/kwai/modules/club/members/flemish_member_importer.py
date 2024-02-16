"""Module for defining an importer for members of the Flemish Judo Federation."""
import csv
from typing import Any, AsyncGenerator

from kwai.core.domain.value_objects.date import Date
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.owner import Owner
from kwai.modules.club.members.country_repository import CountryRepository
from kwai.modules.club.members.member import MemberEntity
from kwai.modules.club.members.member_importer import MemberImporter
from kwai.modules.club.members.value_objects import Birthdate, Gender, License


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

    async def import_(self) -> AsyncGenerator[MemberEntity, None]:
        with open(self._filename) as csv_file:
            member_reader = csv.DictReader(csv_file)
            row: dict[str, Any]
            for row in member_reader:
                if row["geslacht"] == "V":
                    gender = Gender.FEMALE
                elif row["geslacht"] == "M":
                    gender = Gender.MALE
                else:
                    gender = Gender.UNKNOWN

                country = await self._get_country(
                    self._country_repo, row["nationaliteit"]
                )
                if country is None:
                    continue

                yield MemberEntity(
                    name=Name(first_name=row["voornaam"], last_name=row["achternaam"]),
                    license=License(
                        number=row["vergunning"],
                        end_date=Date.create_from_string(row["vervaldatum"]),
                    ),
                    gender=gender,
                    birthdate=Birthdate(
                        date=Date.create_from_string(row["geboortedatum"])
                    ),
                    nationality=country,
                    active=row["status"] == "ACTIEF",
                )
        self._get_country.cache_clear()
