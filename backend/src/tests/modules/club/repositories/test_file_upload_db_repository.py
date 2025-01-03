"""Module for testing the file upload repository."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.owner import Owner
from kwai.modules.club.domain.file_upload import FileUploadEntity
from kwai.modules.club.repositories.file_upload_db_repository import (
    FileUploadDbRepository,
)

pytestmark = pytest.mark.db


async def test_create(database: Database, owner: Owner):
    """Test the creation of a file upload entity."""
    file_upload = FileUploadEntity(
        filename="test.csv",
        owner=owner,
    )
    file_upload = await FileUploadDbRepository(database).create(file_upload)
    assert file_upload.id is not None
