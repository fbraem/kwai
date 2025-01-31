"""Module for testing the use case Revoke User."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.presenter import Presenter
from kwai.modules.identity.revoke_user import RevokeUser, RevokeUserCommand
from kwai.modules.identity.tokens.user_token_db_repository import UserTokenDbRepository
from kwai.modules.identity.users.user_account import UserAccountEntity
from kwai.modules.identity.users.user_account_db_repository import (
    UserAccountDbRepository,
)


pytestmark = pytest.mark.db


class DummyPresenter(Presenter[UserAccountEntity]):
    """A dummy presenter for testing RevokeUser."""

    def __init__(self):
        self._entity = None

    def present(self, use_case_result: UserAccountEntity) -> None:
        self._entity = use_case_result

    @property
    def entity(self) -> UserAccountEntity:
        """Return the entity returned by the use case."""
        return self._entity


async def test_revoke_user(database: Database, make_user_account_in_db):
    """Test the revoke user use case."""
    user_account_in_db = await make_user_account_in_db()

    user_account_repo = UserAccountDbRepository(database)
    user_token_repo = UserTokenDbRepository(database)
    command = RevokeUserCommand(uuid=str(user_account_in_db.user.uuid))
    presenter = DummyPresenter()

    await RevokeUser(user_account_repo, user_token_repo, presenter).execute(command)

    assert presenter.entity.revoked is True, "The user account should be revoked"
