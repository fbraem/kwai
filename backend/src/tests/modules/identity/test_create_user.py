"""Test the use case 'create user'."""
import pytest

from kwai.core.db.database import Database
from kwai.modules.identity.create_user import CreateUser, CreateUserCommand
from kwai.modules.identity.users.user_account_db_repository import (
    UserAccountDbRepository,
)

pytestmark = pytest.mark.integration


@pytest.mark.asyncio
async def test_create_user(database: Database):
    """Test the use case CreateUser."""
    user_account_repo = UserAccountDbRepository(database)
    command = CreateUserCommand(
        email="ichiro.abe@kwai.com",
        first_name="Ichiro",
        last_name="Abe",
        password="Test/1234",
        remark="Created with pytest 'test_create_user'",
    )
    user_account = await CreateUser(user_account_repo).execute(command)
    assert user_account is not None, "There should be a user account"

    # Cleanup: delete the user account
    await user_account_repo.delete(user_account)
