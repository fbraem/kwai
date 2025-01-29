"""Module for testing the user account database repository."""

import pytest

from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.modules.identity.users.user_account_db_repository import (
    UserAccountDbRepository,
)
from kwai.modules.identity.users.user_account_repository import (
    UserAccountNotFoundException,
    UserAccountRepository,
)


pytestmark = pytest.mark.db


@pytest.fixture(scope="module")
def repo(database: Database) -> UserAccountRepository:
    """Fixture for creating the repository."""
    return UserAccountDbRepository(database)


async def test_create(make_user_account_in_db):
    """Test if the user account is created."""
    user_account = await make_user_account_in_db()
    assert user_account.id, "There should be a user account entity"


async def test_get_all(repo: UserAccountRepository, make_user_account_in_db):
    """Test if user accounts are retrieved."""
    await make_user_account_in_db()
    user_account = await anext(repo.get_all())
    assert user_account is not None, "There should be a user account entity"


async def test_get_by_email(repo: UserAccountRepository, make_user_account_in_db):
    """Test if the user account can be fetched with email address."""
    user_account = await make_user_account_in_db()
    result = await repo.get_user_by_email(user_account.user.email)
    assert result, "There should be a user account with the given email"


async def test_exists_with_email(repo: UserAccountRepository, make_user_account_in_db):
    """Test if the user account exists with the given email address."""
    user_account = await make_user_account_in_db()
    exists = await repo.exists_with_email(user_account.user.email)
    assert exists, "There should be a user account with the given email"


async def test_get_by_uuid(repo: UserAccountRepository, make_user_account_in_db):
    """Test if the user account can be fetched with a unique id."""
    user_account = await make_user_account_in_db()
    result = await repo.get_user_by_uuid(user_account.user.uuid)
    assert result, "There should be a user account with the given uuid"


async def test_update(
    database: Database, repo: UserAccountRepository, make_user_account_in_db
):
    """Test if the user account can be updated."""
    user_account = await make_user_account_in_db()
    user_account = user_account.revoke()
    async with UnitOfWork(database):
        await repo.update(user_account)
    result = await repo.get_user_by_email(user_account.user.email)
    assert result.revoked is True, "The user should be revoked"


async def test_delete(
    database: Database, repo: UserAccountRepository, make_user_account_in_db
):
    """Test if the user account can be deleted."""
    user_account = await make_user_account_in_db()
    async with UnitOfWork(database):
        await repo.delete(user_account)

    with pytest.raises(UserAccountNotFoundException):
        await repo.get_user_by_email(user_account.user.email)
