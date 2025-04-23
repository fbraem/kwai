"""Module for testing the author database repository."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.portal.repositories.author_db_repository import AuthorDbRepository


pytestmark = [pytest.mark.db]


async def test_create_author(database: Database, make_author, make_user_account_in_db):
    """Test saving an author."""
    author = make_author(user_account=await make_user_account_in_db())
    author = await AuthorDbRepository(database).create(author)
    assert author is not None, "There should be an author"


async def test_get_author(database: Database, make_author_in_db):
    """Test fetching an author."""
    author = await make_author_in_db()
    uuid = author.uuid
    author = await AuthorDbRepository(database).get(author.id)
    assert author is not None, "There should be an author"
    assert author.uuid == uuid, "The unique id should be the same"


async def test_get_author_by_uuid(
    database: Database, make_author_in_db, make_user_account_in_db
):
    """Test fetching an author."""
    user_account = await make_user_account_in_db()
    author = await make_author_in_db(user_account=user_account)
    author = await AuthorDbRepository(database).get_by_uuid(user_account.user.uuid)
    assert author is not None, "There should be an author with the given uuid"
