"""Module that defines an interface for a file upload repository."""

from abc import ABC, abstractmethod

from kwai.modules.club.domain.file_upload import FileUploadEntity
from kwai.modules.club.domain.member import MemberEntity


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

    @abstractmethod
    async def save_member(self, file_upload: FileUploadEntity, member: MemberEntity):
        """Save a member imported from the file upload.

        Args:
            file_upload: The file upload.
            member: The member from the file upload.
        """
        raise NotImplementedError
