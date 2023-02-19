"""Module for testing the user account database repository."""
from random import randint

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.password import Password
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.identity.users.user_account import UserAccountEntity
from kwai.modules.identity.users.user_account_db_repository import (
    UserAccountDbRepository,
)
from kwai.modules.identity.users.user_account_repository import (
    UserAccountRepository,
    UserAccountNotFoundException,
)

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def repo(database: Database) -> UserAccountRepository:
    """Fixture for creating the repository."""
    return UserAccountDbRepository(database)


@pytest.fixture(scope="module")
def user_account(repo: UserAccountRepository):
    """Fixture for creating a user account."""
    number = randint(1, 99)
    email = f"jigoro.kano{number:02d}@kwai.com"
    user_account = UserAccountEntity(
        password=Password.create_from_string("Test1234"),
        user=UserEntity(
            email=EmailAddress(email),
            name=Name(first_name="Jigoro", last_name="Kano"),
        ),
    )
    return repo.create(user_account)


def test_create(user_account: UserAccountEntity):
    """Test if the user account is created."""
    assert user_account.id, "There should be a user account entity"


def test_get_by_email(repo: UserAccountRepository, user_account: UserAccountEntity):
    """Test if the user account can be fetched with email address."""
    result = repo.get_user_by_email(user_account.user.email)
    assert result, "There should be a user account with the given email"


def test_update(repo: UserAccountRepository, user_account: UserAccountEntity):
    """Test if the user account can be updated."""
    user_account.revoke()
    repo.update(user_account)
    result = repo.get_user_by_email(user_account.user.email)
    assert result.revoked is True, "The user should be revoked"


def test_delete(repo: UserAccountRepository, user_account: UserAccountEntity):
    """Test if the user account can be deleted."""
    repo.delete(user_account)

    with pytest.raises(UserAccountNotFoundException):
        repo.get_user_by_email(user_account.user.email)
