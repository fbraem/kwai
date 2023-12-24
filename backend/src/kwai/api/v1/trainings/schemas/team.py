"""Module that defines the team schema."""
from types import NoneType

from pydantic import BaseModel

from kwai.api.schemas.resources import TeamResourceIdentifier
from kwai.core.json_api import Document, ResourceData
from kwai.modules.training.teams.team import TeamEntity


class TeamAttributes(BaseModel):
    """Attributes for a team JSON:API resource."""

    name: str


class TeamResource(TeamResourceIdentifier, ResourceData[TeamAttributes, NoneType]):
    """A JSON:API resource for a team."""


class TeamDocument(Document[TeamResource, NoneType]):
    """A JSON:API document for one or more teams."""

    @classmethod
    def create(cls, team: TeamEntity) -> "TeamDocument":
        """Create a document from a team entity."""
        return TeamDocument(
            data=TeamResource(
                id=str(team.id), attributes=TeamAttributes(name=team.name)
            )
        )
