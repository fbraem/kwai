"""Module that implements the use case 'Get Teams'."""

from dataclasses import dataclass

from kwai.core.domain.presenter import AsyncPresenter, IterableResult
from kwai.modules.teams.domain.team import TeamEntity
from kwai.modules.teams.repositories.team_repository import TeamRepository


@dataclass(kw_only=True, frozen=True, slots=True)
class GetTeamsCommand:
    """Input for the use case 'Get Teams'."""

    offset: int | None = None
    limit: int | None = None


class GetTeams:
    """Implement the use case 'Get Teams'."""

    def __init__(
        self,
        team_repo: TeamRepository,
        presenter: AsyncPresenter[IterableResult[TeamEntity]],
    ):
        """Initialize the use case."""
        self._team_repo = team_repo
        self._presenter = presenter

    async def execute(self, command: GetTeamsCommand) -> None:
        """Execute the use case."""
        query = self._team_repo.create_query()
        await self._presenter.present(
            IterableResult(
                count=await query.count(),
                limit=command.limit,
                offset=command.offset,
                iterator=self._team_repo.get_all(query, command.offset, command.limit),
            )
        )
