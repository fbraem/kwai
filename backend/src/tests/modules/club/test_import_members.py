"""Module for testing the use case Import Members."""
from pathlib import Path

from kwai.core.db.database import Database
from kwai.modules.club.import_members import ImportMembers
from kwai.modules.club.members.country_db_repository import CountryDbRepository
from kwai.modules.club.members.flemish_member_importer import FlemishMemberImporter


async def test_import_members(database: Database):
    """Test the use case Import Members."""
    filename = Path(__file__).parent / "members" / "data" / "flemish_members_test.csv"

    importer = FlemishMemberImporter(str(filename), CountryDbRepository(database))
    result = await ImportMembers(importer).execute()
    member = await anext(result.iterator)
    print(member.name)
