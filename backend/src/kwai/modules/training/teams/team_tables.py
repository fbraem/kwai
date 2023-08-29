"""Module that defines all dataclasses for the team tables."""
from dataclasses import dataclass

from kwai.core.db.table import Table
from kwai.modules.training.teams.team import TeamEntity, TeamIdentifier


@dataclass(kw_only=True, frozen=True, slots=True)
class TeamRow:
    """Represent a row of the teams table."""

    id: int
    name: str

    def create_entity(self) -> TeamEntity:
        """Create a Team entity of this row."""
        return TeamEntity(id_=TeamIdentifier(self.id), name=self.name)


TeamsTable = Table("teams", TeamRow)
