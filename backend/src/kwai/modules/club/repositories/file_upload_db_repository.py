"""Module that implements a FileUploadRepository using a database."""

from kwai.core.db.database import Database
from kwai.core.domain.entity import Entity
from kwai.modules.club.domain.file_upload import FileUploadEntity, FileUploadIdentifier
from kwai.modules.club.repositories._member_tables import FileUploadRow
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
        await self._database.commit()
        return Entity.replace(file_upload, id_=FileUploadIdentifier(new_id))
