"""Module for testing the use case authenticate user."""
from kwai.core.db.database import Database
from kwai.modules.identity.authenticate_user import (
    AuthenticateUserCommand,
    AuthenticateUser,
)
from kwai.modules.identity.tokens.access_token_db_repository import (
    AccessTokenDbRepository,
)
from kwai.modules.identity.tokens.refresh_token_db_repository import (
    RefreshTokenDbRepository,
)
from kwai.modules.identity.users.user_account import UserAccountEntity
from kwai.modules.identity.users.user_account_db_repository import (
    UserAccountDbRepository,
)


def test_authenticate_user(database: Database, user_account: UserAccountEntity):
    """Test the use case authenticate user."""
    command = AuthenticateUserCommand(
        username=str(user_account.user.email), password="Nage-waza/1882"
    )

    refresh_token = AuthenticateUser(
        UserAccountDbRepository(database),
        AccessTokenDbRepository(database),
        RefreshTokenDbRepository(database),
    ).execute(command)

    assert refresh_token is not None, "There should be a refresh token"
