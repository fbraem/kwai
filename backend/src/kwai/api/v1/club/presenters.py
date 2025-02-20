"""Module that defines presenters for the club api."""

from kwai.api.v1.club.schemas.member import MemberDocument
from kwai.core.domain.presenter import AsyncPresenter, IterableResult, Presenter
from kwai.core.json_api import Error, ErrorSource, JsonApiPresenter, Meta
from kwai.modules.club.domain.member import MemberEntity
from kwai.modules.club.import_members import (
    FailureMemberImportResult,
    MemberImportResult,
    OkMemberImportResult,
)


class JsonApiMemberPresenter(JsonApiPresenter[MemberDocument], Presenter[MemberEntity]):
    """A presenter that transform a member entity into a JSON:API document."""

    def present(self, member: MemberEntity) -> None:
        self._document = MemberDocument.create(member)


class JsonApiMembersPresenter(
    JsonApiPresenter[MemberDocument], AsyncPresenter[IterableResult[MemberEntity]]
):
    """A presenter that transform an iterator for members into a JSON:API document."""

    async def present(self, result: IterableResult[MemberEntity]) -> None:
        self._document = MemberDocument(
            meta=Meta(count=result.count, offset=result.offset, limit=result.limit),
            data=[],
        )
        async for member in result.iterator:
            member_document = MemberDocument.create(member)
            self._document.merge(member_document)


class JsonApiUploadMemberPresenter(
    JsonApiPresenter[MemberDocument], Presenter[MemberImportResult]
):
    """A presenter that transform a file upload of a member into a JSON:API document."""

    def __init__(self) -> None:
        super().__init__()
        self._document = MemberDocument(
            meta=Meta(count=0, offset=0, limit=0), data=[], errors=[]
        )

    def present(self, result: MemberImportResult) -> None:
        match result:
            case OkMemberImportResult():
                member_document = MemberDocument.create(result.member)
                member_document.resource.meta.row = result.row
                member_document.resource.meta.new = not result.member.has_id()
                # A new member has related resources that are not saved yet,
                # so give them temporarily the same id as the member.
                if member_document.resource.meta.new:
                    member_document.resource.relationships.person.data.id = (
                        member_document.resource.id
                    )
                    for included in member_document.included:
                        if included.type == "persons":
                            included.relationships.contact.data.id = (
                                member_document.resource.id
                            )
                        if included.id == "0":
                            included.id = member_document.resource.id
                self._document.meta.count += 1
                self._document.merge(member_document)
            case FailureMemberImportResult():
                self._document.errors.append(
                    Error(
                        source=ErrorSource(pointer=str(result.row)),
                        detail=result.to_message(),
                    )
                )
