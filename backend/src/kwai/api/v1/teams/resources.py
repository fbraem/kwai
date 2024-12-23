"""Module that defines all JSON:API resource identifiers for the team API."""

from typing import Literal

from kwai.core.json_api import ResourceIdentifier


class TeamMemberResourceIdentifier(ResourceIdentifier):
    """A JSON:API resource identifier for a team member."""

    type: Literal["team_members"] = "team_members"
