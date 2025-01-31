"""Module that defines the use case for revoking a user."""

from dataclasses import dataclass

from kwai.core.domain.presenter import Presenter
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.tokens.user_token_repository import UserTokenRepository
from kwai.modules.identity.users.user_account import UserAccountEntity
from kwai.modules.identity.users.user_account_repository import UserAccountRepository


@dataclass(frozen=True, kw_only=True, slots=True)
class RevokeUserCommand:
    """Input for the RevokeUser use case.

    Attributes:
        uuid: The UUID of the user to revoke.
    """

    uuid: str


class RevokeUser:
    """Use case for revoking a user."""

    def __init__(
        self,
        repo: UserAccountRepository,
        user_token_repo: UserTokenRepository,
        presenter: Presenter[UserAccountEntity],
    ):
        """Initialize the use case.

        Args:
            repo: The user account repository to use.
            user_token_repo: The user token repository to use.
            presenter: The presenter that will be used to return the user.
        """
        self._repo = repo
        self._user_token_repo = user_token_repo
        self._presenter = presenter

    async def execute(self, command: RevokeUserCommand):
        """Execute the use case.

        Raises:
            UserAccountNotFoundException: If the user does not exist.
        """
        user_account = await self._repo.get_user_by_uuid(
            UniqueId.create_from_string(command.uuid)
        )
        user_account = user_account.revoke()
        await self._repo.update(user_account)
        await self._user_token_repo.revoke(user_account)
        self._presenter.present(user_account)
