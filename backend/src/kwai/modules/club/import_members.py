"""Module that implements a use case for importing members."""
from dataclasses import dataclass

from kwai.core.domain.use_case import UseCaseResult
from kwai.modules.club.members.file_upload import FileUploadEntity
from kwai.modules.club.members.file_upload_repository import FileUploadRepository
from kwai.modules.club.members.member_importer import MemberImporter


@dataclass(kw_only=True, slots=True, frozen=True)
class ImportMembersResult(UseCaseResult):
    """The result of the use case ImportMembers."""

    file_upload: FileUploadEntity

    def to_message(self) -> str:
        return ""


class ImportMembers:
    """Use case for importing members."""

    def __init__(
        self, importer: MemberImporter, file_upload_repo: FileUploadRepository
    ):
        """Initialize the use case.

        Args:
            importer: A class that is responsible for importing members from a resource.
            file_upload_repo: A repository for storing the file upload information.
        """
        self._importer = importer
        self._file_upload_repo = file_upload_repo

    async def execute(self) -> ImportMembersResult:
        """Execute the use case."""
        file_upload_entity = await self._file_upload_repo.create(
            self._importer.create_file_upload_entity()
        )
        async for member in self._importer.import_():
            print(member)

        result = ImportMembersResult(file_upload=file_upload_entity)

        return result
