"""Module for testing the use case Import Members."""

from pathlib import Path

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.owner import Owner
from kwai.modules.club.import_members import ImportMembers, ImportMembersCommand
from kwai.modules.club.members.country_db_repository import CountryDbRepository
from kwai.modules.club.members.file_upload_db_repository import FileUploadDbRepository
from kwai.modules.club.members.flemish_member_importer import FlemishMemberImporter
from kwai.modules.club.members.member_db_repository import MemberDbRepository


async def test_import_members(database: Database, owner: Owner):
    """Test the use case Import Members."""
    filename = Path(__file__).parent / "members" / "data" / "flemish_members_test.csv"

    importer = FlemishMemberImporter(
        str(filename), owner, CountryDbRepository(database)
    )

    command = ImportMembersCommand()
    async for result in ImportMembers(
        importer, FileUploadDbRepository(database), MemberDbRepository(database)
    ).execute(command):
        assert result.file_upload is not None, "There should be a fileupload result"
