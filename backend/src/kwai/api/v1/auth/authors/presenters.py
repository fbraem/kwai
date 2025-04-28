"""Module for defining presenters for JSON:API author documents."""

from kwai.api.v1.auth.authors.schemas import (
    AuthorDocument,
    AuthorResource,
    AuthorsDocument,
)
from kwai.core.domain.presenter import AsyncPresenter, IterableResult
from kwai.core.json_api import JsonApiPresenter, Meta
from kwai.modules.portal.domain.author import AuthorEntity


class JsonApiAuthorsPresenter(
    JsonApiPresenter[AuthorsDocument],
    AsyncPresenter[IterableResult[AuthorEntity]],
):
    """A presenter that transform an iterable list of author entities into a JSON:API document."""

    async def present(self, result: IterableResult[AuthorEntity]) -> None:
        self._document = AuthorsDocument(
            meta=Meta(count=result.count, offset=result.offset, limit=result.limit),
            data=[],
        )
        async for author in result.iterator:
            self._document.merge(AuthorDocument(data=AuthorResource.create(author)))
