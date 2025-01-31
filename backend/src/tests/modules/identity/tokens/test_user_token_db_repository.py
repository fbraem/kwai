"""Module for testing the user token repository for a database."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.identity.tokens.user_token_db_repository import UserTokenDbRepository


pytestmark = pytest.mark.db


async def test_revoke(database: Database, make_user_account_in_db):
    """Test revoking access and refresh tokens of a user account."""
    user_account = await make_user_account_in_db()

    repo = UserTokenDbRepository(database)
    try:
        await repo.revoke(user_account)
    except Exception as exc:
        pytest.fail(f"Revoke failed with exception: {exc}")
