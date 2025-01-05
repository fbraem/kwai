"""Module that defines a file upload repository that can be used for preview."""

from kwai.modules.club.domain.file_upload import FileUploadEntity
from kwai.modules.club.domain.member import MemberEntity
from kwai.modules.club.repositories.file_upload_repository import (
    DuplicateMemberUploadedException,
    FileUploadRepository,
)


class FileUploadPreviewRepository(FileUploadRepository):
    """A file upload repository that can be used for preview.

    This implementation doesn't save anything to the database.
    """

    def __init__(self):
        self._saved_members: dict[str, MemberEntity] = {}

    async def create(self, file_upload: FileUploadEntity) -> FileUploadEntity: ...

    def is_duplicate(self, member: MemberEntity) -> bool:
        return member.license.number in self._saved_members

    async def save_member(self, file_upload: FileUploadEntity, member: MemberEntity):
        if self.is_duplicate(member):
            raise DuplicateMemberUploadedException(
                f"Member with license {member.license.number} is already uploaded."
            )
        self._saved_members[member.license.number] = member
