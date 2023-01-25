"""Module with tests for the user database repository."""
from random import randint

import pytest

from kwai.core.db import Database
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.password import Password
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.users.user import User
from kwai.modules.identity.users.user_account import UserAccount, UserAccountEntity
from kwai.modules.identity.users.user_account_db_repository import (
    UserAccountDbRepository,
)
from kwai.modules.identity.users.user_db_repository import UserDbRepository
from kwai.modules.identity.users.user_repository import (
    UserRepository,
    UserNotFoundException,
)


@pytest.fixture(scope="module")
def repo(database: Database) -> UserRepository:
    """Fixture for creating a repository."""
    return UserDbRepository(database)


@pytest.fixture(scope="module")
def user_account(database):
    """Fixture for creating a user account.

    The user repository does not provide a way to create a user. So, we need
    to use the UserAccountRepository here.
    """
    number = randint(1, 99)
    email = f"jigoro.kano{number:02d}@kwai.com"
    user_account = UserAccount(
        password=Password.create_from_string("Test1234"),
        user=User(
            uuid=UniqueId.generate(),
            email=EmailAddress(email),
            name=Name(first_name="Jigoro", last_name="Kano"),
        ),
    )
    return UserAccountDbRepository(database).create(user_account)


def test_create(user_account: UserAccountEntity):
    """Test if the user account is created."""
    assert user_account.id, "There should be a user account entity"


def test_get_by_id(repo: UserRepository, user_account: UserAccountEntity):
    """Test if the user can be fetched with an id."""
    result = repo.get_user_by_id(user_account.id)
    assert result, "There should be a user with the given id"


def test_get_by_uuid(repo: UserRepository, user_account: UserAccountEntity):
    """Test if the user can be fetched with an uuid."""
    result = repo.get_user_by_uuid(user_account().user.uuid)
    assert result, "There should be a user with the given uuid"


def test_get_by_email(repo: UserRepository, user_account: UserAccountEntity):
    """Test if the user can be fetched with email address."""
    result = repo.get_user_by_email(user_account().user.email)
    assert result, "There should be a user with the given email"


def test_delete(
    repo: UserRepository, database: Database, user_account: UserAccountEntity
):
    """Test if the user can be deleted."""
    UserAccountDbRepository(database).delete(user_account)

    with pytest.raises(UserNotFoundException):
        repo.get_user_by_email(user_account().user.email)
