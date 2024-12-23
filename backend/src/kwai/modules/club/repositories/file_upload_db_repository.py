"""Module that implements a FileUploadRepository using a database."""

from kwai.core.db.database import Database
from kwai.core.domain.entity import Entity
from kwai.modules.club.domain.file_upload import FileUploadEntity, FileUploadIdentifier
from kwai.modules.club.domain.member import MemberEntity
from kwai.modules.club.repositories._tables import FileUploadRow, MemberUploadRow
from kwai.modules.club.repositories.file_upload_repository import FileUploadRepository


class FileUploadDbRepository(FileUploadRepository):
    """An implementation of a FileUploadRepository using a database."""

    def __init__(self, database: Database):
        """Initialize the repository.

        Args:
            database: The database for this repository.
        """
        self._database = database

    async def create(self, file_upload: FileUploadEntity) -> FileUploadEntity:
        new_id = await self._database.insert(
            FileUploadRow.__table_name__, FileUploadRow.persist(file_upload)
        )
        return Entity.replace(file_upload, id_=FileUploadIdentifier(new_id))

    async def save_member(self, file_upload: FileUploadEntity, member: MemberEntity):
        await self._database.insert(
            MemberUploadRow.__table_name__,
            MemberUploadRow.persist(file_upload, member),
        )
