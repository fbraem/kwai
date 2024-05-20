"""Module that defines an interface for a file upload repository."""

from abc import ABC, abstractmethod

from kwai.modules.club.domain.file_upload import FileUploadEntity


class FileUploadRepository(ABC):
    """Interface for an import repository.

    An import repository registers file uploads.
    """

    @abstractmethod
    async def create(self, file_upload: FileUploadEntity) -> FileUploadEntity:
        """Save a fileupload.

        Args:
            file_upload: A fileupload to save.
        """
        raise NotImplementedError
