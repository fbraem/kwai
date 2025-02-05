"""Module for testing the use case Enact User."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.presenter import Presenter
from kwai.modules.identity.enact_user import EnactUser, EnactUserCommand
from kwai.modules.identity.users.user_account import UserAccountEntity
from kwai.modules.identity.users.user_account_db_repository import (
    UserAccountDbRepository,
)


pytestmark = pytest.mark.db


class DummyPresenter(Presenter[UserAccountEntity]):
    """A dummy presenter for testing EnactUser."""

    def __init__(self):
        self._entity = None

    def present(self, use_case_result: UserAccountEntity) -> None:
        self._entity = use_case_result

    @property
    def entity(self) -> UserAccountEntity:
        """Return the entity returned by the use case."""
        return self._entity


async def test_enact_user(database: Database, make_user_account_in_db):
    """Test the revoke user use case."""
    user_account_in_db = await make_user_account_in_db()

    user_account_repo = UserAccountDbRepository(database)
    command = EnactUserCommand(uuid=str(user_account_in_db.user.uuid))
    presenter = DummyPresenter()

    await EnactUser(user_account_repo, presenter).execute(command)

    assert presenter.entity.revoked is False, "The user account should be active"
