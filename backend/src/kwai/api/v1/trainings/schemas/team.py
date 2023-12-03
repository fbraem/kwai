"""Module that defines the team schema."""
from kwai.core import json_api
from kwai.modules.training.teams.team import TeamEntity


@json_api.resource(type_="teams")
class TeamResource:
    """Represent a team."""

    def __init__(self, team: TeamEntity):
        self._team = team

    @json_api.id
    def get_id(self) -> str:
        """Return the id of the team."""
        return str(self._team.id)

    @json_api.attribute(name="name")
    def get_name(self) -> str:
        """Return the name of the team."""
        return self._team.name
