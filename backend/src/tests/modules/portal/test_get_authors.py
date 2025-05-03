"""Module for testing the use case 'get authors'."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.presenter import CountIterableAsyncPresenter
from kwai.modules.portal.domain.author import AuthorEntity
from kwai.modules.portal.get_authors import GetAuthors, GetAuthorsCommand
from kwai.modules.portal.repositories.author_db_repository import AuthorDbRepository


pytestmark = [pytest.mark.db]


async def test_get_authors(database: Database, make_author_in_db):
    """Test the 'get authors' use case."""
    await make_author_in_db()
    command = GetAuthorsCommand()
    presenter = CountIterableAsyncPresenter[AuthorEntity]()
    await GetAuthors(AuthorDbRepository(database), presenter).execute(command)
    assert presenter.count == 1, "There should be 1 author"
