"""Module that implements a use case for importing members."""

from abc import ABC
from dataclasses import dataclass

from kwai.core.domain.entity import Entity
from kwai.core.domain.presenter import Presenter
from kwai.core.domain.use_case import UseCaseResult
from kwai.modules.club.domain.file_upload import FileUploadEntity
from kwai.modules.club.domain.member import MemberEntity
from kwai.modules.club.repositories import member_importer
from kwai.modules.club.repositories.file_upload_repository import FileUploadRepository
from kwai.modules.club.repositories.member_repository import (
    MemberNotFoundException,
    MemberRepository,
)


@dataclass(kw_only=True, slots=True, frozen=True)
class MemberImportResult(UseCaseResult, ABC):
    """The result of the use case ImportMembers."""

    file_upload: FileUploadEntity
    row: int


@dataclass(kw_only=True, slots=True, frozen=True)
class OkMemberImportResult(MemberImportResult):
    """A successful import of a member."""

    member: MemberEntity

    def to_message(self) -> str:
        return f"Member {self.member.id}(row={self.row}) imported successfully."


@dataclass(kw_only=True, slots=True, frozen=True)
class FailureMemberImportResult(MemberImportResult):
    """An import of a member failed."""

    message: str

    def to_message(self) -> str:
        return f"Import failed for row {self.row}: {self.message}."


@dataclass(kw_only=True, slots=True, frozen=True)
class ImportMembersCommand:
    """Input for the use case "ImportMembers"."""

    preview: bool = True


class ImportMembers:
    """Use case for importing members."""

    def __init__(
        self,
        importer: member_importer.MemberImporter,
        file_upload_repo: FileUploadRepository,
        member_repo: MemberRepository,
        presenter: Presenter,
    ):
        """Initialize the use case.

        Args:
            importer: A class that is responsible for importing members from a resource.
            file_upload_repo: A repository for storing the file upload information.
            member_repo: A repository for managing members.
            presenter: A presenter
        """
        self._importer = importer
        self._file_upload_repo = file_upload_repo
        self._member_repo = member_repo
        self._presenter = presenter

    async def execute(self, command: ImportMembersCommand):
        """Execute the use case."""
        file_upload_entity = await self._file_upload_repo.create(
            self._importer.create_file_upload_entity(command.preview)
        )
        async for import_result in self._importer.import_():
            match import_result:
                case member_importer.OkResult():
                    member = await self._save_member(
                        file_upload_entity, import_result.member, command.preview
                    )
                    self._presenter.present(
                        OkMemberImportResult(
                            file_upload=file_upload_entity,
                            row=import_result.row,
                            member=member,
                        )
                    )
                case member_importer.FailureResult():
                    self._presenter.present(
                        FailureMemberImportResult(
                            file_upload=file_upload_entity,
                            row=import_result.row,
                            message=import_result.message,
                        )
                    )

    async def _save_member(
        self, file_upload: FileUploadEntity, member: MemberEntity, preview: bool
    ) -> MemberEntity:
        """Create or update the member."""
        existing_member = await self._get_member(member)
        if existing_member is not None:
            updated_member = self._update_member(existing_member, member)
            if not preview:
                await self._member_repo.update(updated_member)
                await self._file_upload_repo.save_member(file_upload, updated_member)
            return updated_member

        if not preview:
            member = await self._member_repo.create(member)
            await self._file_upload_repo.save_member(file_upload, member)
        return member

    @classmethod
    def _update_member(
        cls, old_member: MemberEntity, new_member: MemberEntity
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
            uuid=old_member.uuid,
            remark=old_member.remark,
            competition=old_member.is_competitive,
            active=old_member.is_active,
            person=updated_person,
            traceable_time=old_member.traceable_time.mark_for_update(),
        )
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
