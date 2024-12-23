"""Module that defines the use case 'Create Team'."""

from dataclasses import dataclass

from kwai.core.domain.presenter import Presenter
from kwai.modules.teams.domain.team import TeamEntity
from kwai.modules.teams.repositories.team_repository import TeamRepository


@dataclass(kw_only=True, frozen=True, slots=True)
class CreateTeamCommand:
    """Input for the use case 'Create Team'."""

    name: str
    active: bool
    remark: str


class CreateTeam:
    """Use case 'Create Team'."""

    def __init__(self, team_repo: TeamRepository, presenter: Presenter[TeamEntity]):
        """Initialize the use case.

        Args:
            team_repo: A repository that creates the team.
            presenter: A presenter for a team entity.
        """
        self._team_repo = team_repo
        self._presenter = presenter

    async def execute(self, command: CreateTeamCommand) -> None:
        """Executes the use case."""
        team = TeamEntity(
            name=command.name, active=command.active, remark=command.remark
        )
        self._presenter.present(await self._team_repo.create(team))
