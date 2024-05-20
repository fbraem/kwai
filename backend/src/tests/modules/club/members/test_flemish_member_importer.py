"""Module for testing the FlemishMemberImporter class."""

from pathlib import Path

import pytest
from kwai.core.db.database import Database
from kwai.core.domain.value_objects.owner import Owner
from kwai.modules.club.domain.value_objects import Gender
from kwai.modules.club.members.country_db_repository import CountryDbRepository
from kwai.modules.club.members.flemish_member_importer import FlemishMemberImporter
from kwai.modules.club.members.member_importer import Result

pytestmark = pytest.mark.db


async def test_import(database: Database, owner: Owner):
    """Test the import of members of the Flemish federation."""
    filename = Path(__file__).parent / "data" / "flemish_members_test.csv"
    importer = FlemishMemberImporter(
        str(filename), owner, CountryDbRepository(database)
    )
    members = importer.import_()

    result = await anext(members)
    match result:
        case Result():
            member = result.member
            assert member is not None
            assert str(member.person.nationality) == "BE"
            assert str(member.person.birthdate) == "1973-06-05"
            assert member.person.gender == Gender.FEMALE
    result = await anext(members)
    match result:
        case Result():
            member = result.member
            assert member is not None
            assert str(member.person.nationality) == "JP"
            assert member.person.gender == Gender.MALE
