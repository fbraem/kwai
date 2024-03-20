"""Module that implements a use case for importing members."""

from abc import ABC
from dataclasses import dataclass
from typing import AsyncGenerator

from kwai.core.domain.entity import Entity
from kwai.core.domain.use_case import UseCaseResult
from kwai.modules.club.members import member_importer
from kwai.modules.club.members.file_upload import FileUploadEntity
from kwai.modules.club.members.file_upload_repository import FileUploadRepository
from kwai.modules.club.members.member import MemberEntity
from kwai.modules.club.members.member_repository import (
    MemberNotFoundException,
    MemberRepository,
)


@dataclass(kw_only=True, slots=True, frozen=True)
class Result(UseCaseResult, ABC):
    """The result of the use case ImportMembers."""

    file_upload: FileUploadEntity
    row: int


@dataclass(kw_only=True, slots=True, frozen=True)
class OkResult(Result):
    """A successful import of a member."""

    member: MemberEntity

    def to_message(self) -> str:
        return f"Member {self.member.id}(row={self.row}) imported successfully."


@dataclass(kw_only=True, slots=True, frozen=True)
class FailureResult(Result):
    """An import of a member failed."""

    message: str

    def to_message(self) -> str:
        return f"Import failed for row {self.row}: {self.message}."


class ImportMembers:
    """Use case for importing members."""

    def __init__(
        self,
        importer: member_importer.MemberImporter,
        file_upload_repo: FileUploadRepository,
        member_repo: MemberRepository,
    ):
        """Initialize the use case.

        Args:
            importer: A class that is responsible for importing members from a resource.
            file_upload_repo: A repository for storing the file upload information.
            member_repo: A repository for managing members.
        """
        self._importer = importer
        self._file_upload_repo = file_upload_repo
        self._member_repo = member_repo

    async def execute(self) -> AsyncGenerator[Result, None]:
        """Execute the use case.

        Yields:
            OkResult: When the row was successfully imported.
            FailureResult: When the row was not successfully imported.
        """
        file_upload_entity = await self._file_upload_repo.create(
            self._importer.create_file_upload_entity()
        )
        async for import_result in self._importer.import_():
            match import_result:
                case member_importer.OkResult():
                    member = await self._save_member(import_result.member)
                    yield OkResult(
                        file_upload=file_upload_entity,
                        row=import_result.row,
                        member=member,
                    )
                case member_importer.FailureResult():
                    yield FailureResult(
                        file_upload=file_upload_entity,
                        row=import_result.row,
                        message=import_result.message,
                    )

    async def _save_member(self, member: MemberEntity) -> MemberEntity:
        """Create or update the member."""
        existing_member = await self._get_member(member)
        if existing_member is not None:
            return await self._update_member(existing_member, member)
        return await self._member_repo.create(member)

    async def _update_member(
        self, old_member: MemberEntity, new_member: MemberEntity
    ) -> MemberEntity:
        """Update an existing member with the new imported data."""
        updated_contact = Entity.replace(
            old_member.person.contact,
            id_=old_member.person.contact.id,
            traceable_time=old_member.person.contact.traceable_time.mark_for_update(),
        )
        updated_person = Entity.replace(
            old_member.person,
            id_=old_member.person.id,
            contact=updated_contact,
            traceable_time=old_member.person.traceable_time.mark_for_update(),
        )
        updated_member = Entity.replace(
            new_member,
            id_=old_member.id,
            person=updated_person,
            traceable_time=old_member.traceable_time.mark_for_update(),
        )
        await self._member_repo.update(updated_member)
        return updated_member

    async def _get_member(self, member: MemberEntity) -> MemberEntity | None:
        """Return the member.

        Returns:
            If found the member is returned, otherwise None is returned.
        """
        member_query = self._member_repo.create_query()
        member_query.filter_by_license(member.license.number)

        try:
            member = await self._member_repo.get(member_query)
        except MemberNotFoundException:
            return None

        return member
