"""Module for testing the file upload repository."""

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.owner import Owner
from kwai.modules.club.members.file_upload import FileUploadEntity
from kwai.modules.club.members.file_upload_db_repository import FileUploadDbRepository


async def test_create(database: Database, owner: Owner):
    """Test the creation of a file upload entity."""
    file_upload = FileUploadEntity(
        filename="test.csv",
        owner=owner,
    )
    file_upload = await FileUploadDbRepository(database).create(file_upload)
    assert file_upload.id is not None
