"""Module that defines the use case for enacting a user."""

from dataclasses import dataclass

from kwai.core.domain.presenter import Presenter
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.users.user_account import UserAccountEntity
from kwai.modules.identity.users.user_account_repository import UserAccountRepository


@dataclass(frozen=True, kw_only=True, slots=True)
class EnactUserCommand:
    """Input for the EnactUser use case.

    Attributes:
        uuid: The UUID of the user to enact.
    """

    uuid: str


class EnactUser:
    """Use case for enacting a user."""

    def __init__(
        self,
        repo: UserAccountRepository,
        presenter: Presenter[UserAccountEntity],
    ):
        """Initialize the use case.

        Args:
            repo: The user account repository to use.
            presenter: The presenter that will be used to return the user.
        """
        self._repo = repo
        self._presenter = presenter

    async def execute(self, command: EnactUserCommand) -> None:
        """Execute the use case.

        Raises:
            UserAccountNotFoundException: If the user does not exist.
        """
        user_account = await self._repo.get_user_by_uuid(
            UniqueId.create_from_string(command.uuid)
        )
        user_account = user_account.enact()
        await self._repo.update(user_account)
        self._presenter.present(user_account)
