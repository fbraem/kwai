"""Module that implements the use case 'Get Teams'."""

from dataclasses import dataclass

from kwai.core.domain.presenter import Presenter
from kwai.modules.club.domain.team import TeamEntity
from kwai.modules.training.teams.team_repository import TeamRepository


@dataclass(kw_only=True, frozen=True, slots=True)
class GetTeamsCommand:
    """Input for the use case 'Get Teams'."""

    offset: int
    limit: int


class GetTeams:
    """Implement the use case 'Get Teams'."""

    def __init__(self, team_repo: TeamRepository, presenter: Presenter[TeamEntity]):
        """Initialize the use case."""
        self._team_repo = team_repo
        self._presenter = presenter

    def execute(self, command: GetTeamsCommand) -> None:
        """Execute the use case."""
