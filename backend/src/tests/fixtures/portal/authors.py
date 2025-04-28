"""Module for defining factory fixtures for authors."""

import pytest

from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.modules.identity.users.user_account import UserAccountEntity
from kwai.modules.portal.domain.author import AuthorEntity, AuthorIdentifier
from kwai.modules.portal.repositories.author_db_repository import AuthorDbRepository


@pytest.fixture
def make_author(make_user_account):
    """A factory fixture for creating an author."""

    def _make_author(
        user_account: UserAccountEntity | None = None,
        name: str = "",
        active: bool = True,
        remark: str = "",
    ) -> AuthorEntity:
        the_user_account = user_account or make_user_account()
        return AuthorEntity(
            id=AuthorIdentifier(the_user_account.id),
            uuid=the_user_account.user.uuid,
            name=name,
            active=active,
            remark=remark,
        )

    return _make_author


@pytest.fixture
def make_author_in_db(
    request, event_loop, database: Database, make_author, make_user_account_in_db
):
    """A factory fixture for creating an author in the database."""

    async def _make_author_in_db(
        user_account: UserAccountEntity | None = None,
        author: AuthorEntity | None = None,
    ) -> AuthorEntity:
        user_account = user_account or await make_user_account_in_db()
        author = author or make_author(user_account)
        repo = AuthorDbRepository(database)
        async with UnitOfWork(database):
            author = await repo.create(author)

        def cleanup():
            async def acleanup():
                async with UnitOfWork(database):
                    await repo.delete(author)

            event_loop.run_until_complete(acleanup())

        request.addfinalizer(cleanup)

        return author

    return _make_author_in_db
