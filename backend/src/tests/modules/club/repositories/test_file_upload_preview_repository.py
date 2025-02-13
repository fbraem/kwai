"""Module for testing the file upload preview repository."""

import pytest

from kwai.core.domain.value_objects.owner import Owner
from kwai.modules.club.domain.file_upload import FileUploadEntity
from kwai.modules.club.repositories.file_upload_preview_repository import (
    FileUploadPreviewRepository,
)
from kwai.modules.club.repositories.file_upload_repository import (
    DuplicateMemberUploadedException,
)


async def test_upload(owner: Owner, make_member):
    """Test upload."""
    repo = FileUploadPreviewRepository()
    file_upload = FileUploadEntity(filename="test.csv", owner=owner)
    try:
        await repo.save_member(file_upload, make_member())
    except Exception as error:
        pytest.fail(error)


async def test_duplicate_upload(owner: Owner, make_member):
    """Test if a duplicate member exception is raised when member is uploaded twice."""
    repo = FileUploadPreviewRepository()
    file_upload = FileUploadEntity(filename="test.csv", owner=owner)
    member = make_member()
    with pytest.raises(DuplicateMemberUploadedException):
        await repo.save_member(file_upload, member)
        await repo.save_member(file_upload, member)
