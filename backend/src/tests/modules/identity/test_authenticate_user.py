"""Module for testing the use case authenticate user."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.password import Password
from kwai.modules.identity.authenticate_user import (
    AuthenticateUser,
    AuthenticateUserCommand,
)
from kwai.modules.identity.tokens.access_token_db_repository import (
    AccessTokenDbRepository,
)
from kwai.modules.identity.tokens.log_user_login_db_service import LogUserLoginDbService
from kwai.modules.identity.tokens.refresh_token_db_repository import (
    RefreshTokenDbRepository,
)
from kwai.modules.identity.users.user_account_db_repository import (
    UserAccountDbRepository,
)


pytestmark = pytest.mark.db


async def test_authenticate_user(
    database: Database, make_user_account_in_db, make_user_account
):
    """Test the use case authenticate user."""
    user_account = await make_user_account_in_db(
        make_user_account(password=Password.create_from_string("Nage-waza/1882"))
    )
    command = AuthenticateUserCommand(
        username=str(user_account.user.email), password="Nage-waza/1882"
    )

    refresh_token = await AuthenticateUser(
        UserAccountDbRepository(database),
        AccessTokenDbRepository(database),
        RefreshTokenDbRepository(database),
        LogUserLoginDbService(
            database,
            user_agent="pytest",
            client_ip="127.0.0.1",
            email=str(user_account.user.email),
        ),
    ).execute(command)

    assert refresh_token is not None, "There should be a refresh token"
