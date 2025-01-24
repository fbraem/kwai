"""Module for the get user accounts use case."""

from dataclasses import dataclass

from kwai.core.domain.presenter import AsyncPresenter, IterableResult
from kwai.modules.identity.users.user_account import UserAccountEntity
from kwai.modules.identity.users.user_account_repository import UserAccountRepository


@dataclass(kw_only=True, frozen=True, slots=True)
class GetUserAccountsCommand:
    """Input for the use case.

    Attributes:
        offset: Offset from where to start the query of user accounts.
        limit: The maximum number of users to return.
    """

    offset: int | None = None
    limit: int | None = None


class GetUserAccounts:
    """Implementation of the get user accounts use case."""

    def __init__(
        self,
        user_account_repo: UserAccountRepository,
        presenter: AsyncPresenter[IterableResult[UserAccountEntity]],
    ):
        """Initialize the get users use case."""
        self._user_account_repo = user_account_repo
        self._presenter = presenter

    async def execute(self, command: GetUserAccountsCommand):
        """Execute the get users use case.

        Args:
            command: Input for the use case.
        """
        query = self._user_account_repo.create_query()

        await self._presenter.present(
            IterableResult(
                count=await query.count(),
                limit=command.limit,
                offset=command.offset,
                iterator=self._user_account_repo.get_all(
                    query, command.limit, command.offset
                ),
            )
        )
