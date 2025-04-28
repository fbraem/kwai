"""Module for testing the presenters for the /api/v1/auth/authors endpoint."""

from typing import AsyncGenerator

import pytest

from kwai.api.v1.auth.authors.presenters import JsonApiAuthorsPresenter
from kwai.core.domain.presenter import IterableResult
from kwai.modules.portal.domain.author import AuthorEntity


async def author_iterator(make_author) -> AsyncGenerator[AuthorEntity, None]:
    """A fixture that creates an async iterator with author entities."""
    yield make_author()
    yield make_author()


@pytest.fixture
def iterable_result(make_author) -> IterableResult[AuthorEntity]:
    """A fixture that creates a IterableResult for author entities."""
    return IterableResult[AuthorEntity](count=2, iterator=author_iterator(make_author))


async def test_json_api_authors_presenter(iterable_result):
    """Test a presenter with an iterable result containing authors."""
    presenter = JsonApiAuthorsPresenter()
    await presenter.present(iterable_result)
    document = presenter.get_document()
    assert document is not None, "The presenter should contain a document"
    assert document.meta.count == 2, "Count should be 2"
    assert len(document.data) == 2, "There should be 2 resources"
