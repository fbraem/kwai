"""Module that implements the use case 'Get Team'."""

from dataclasses import dataclass

from kwai.core.domain.presenter import Presenter
from kwai.modules.teams.domain.team import TeamEntity, TeamIdentifier
from kwai.modules.teams.repositories.team_repository import TeamRepository


@dataclass(kw_only=True, frozen=True, slots=True)
class GetTeamCommand:
    """Input for the use case 'Get Team'."""

    id: int


class GetTeam:
    """Implement the use case 'Get Teams'."""

    def __init__(
        self,
        team_repo: TeamRepository,
        presenter: Presenter[TeamEntity],
    ):
        """Initialize the use case."""
        self._team_repo = team_repo
        self._presenter = presenter

    async def execute(self, command: GetTeamCommand) -> None:
        """Execute the use case."""
        query = self._team_repo.create_query()
        query.filter_by_id(TeamIdentifier(command.id))
        self._presenter.present(await self._team_repo.get(query))
