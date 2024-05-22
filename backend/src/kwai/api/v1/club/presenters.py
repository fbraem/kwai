"""Module that defines presenters for the club api."""

from kwai.api.v1.club.schemas.member import MemberDocument
from kwai.core.domain.presenter import AsyncPresenter, IterableResult, Presenter
from kwai.core.json_api import Meta
from kwai.modules.club.domain.member import MemberEntity


class JsonApiPresenter[Document]:
    """An interface for a presenter that generates a JSON:API document."""

    def __init__(self):
        self._document: Document = None

    def get_document(self) -> Document:
        """Return the JSON:API document."""
        return self._document


class JsonApiMemberPresenter(JsonApiPresenter[MemberDocument], Presenter[MemberEntity]):
    """A presenter that transform a member entity into a JSON:API document."""

    def handle(self, member: MemberEntity) -> None:
        self._document = MemberDocument.create(member)


class JsonApiMembersPresenter(
    JsonApiPresenter[MemberDocument], AsyncPresenter[IterableResult[MemberEntity]]
):
    """A presenter that transform an iterator for members into a JSON:API document."""

    async def handle(self, result: IterableResult[MemberEntity]) -> None:
        self._document = MemberDocument(
            meta=Meta(count=result.count, offset=result.offset, limit=result.limit),
            data=[],
        )
        async for member in result.iterator:
            member_document = MemberDocument.create(member)
            self._document.merge(member_document)
