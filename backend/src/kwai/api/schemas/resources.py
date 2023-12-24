"""Module that defines all JSON:API resource identifiers."""
from typing import Literal

from kwai.core.json_api import ResourceIdentifier


class ApplicationResourceIdentifier(ResourceIdentifier):
    """A JSON:API resource identifier for an application."""

    type: Literal["applications"] = "applications"


class PageResourceIdentifier(ResourceIdentifier):
    """A JSON:API resource identifier for a page."""

    type: Literal["pages"] = "pages"


class NewsItemResourceIdentifier(ResourceIdentifier):
    """A JSON:API resource identifier for a news item."""

    type: Literal["news_items"] = "news_items"


class UserInvitationResourceIdentifier(ResourceIdentifier):
    """A JSON:API resource identifier for a user invitation."""

    type: Literal["user_invitations"] = "user_invitations"


class TeamResourceIdentifier(ResourceIdentifier):
    """A JSON:API resource identifier for a team."""

    type: Literal["teams"] = "teams"


class TrainingResourceIdentifier(ResourceIdentifier):
    """A JSON:API resource identifier for a training."""

    type: Literal["trainings"] = "trainings"


class TrainingDefinitionResourceIdentifier(ResourceIdentifier):
    """A JSON:API resource identifier for a training definition."""

    type: Literal["training_definitions"] = "training_definitions"


class CoachResourceIdentifier(ResourceIdentifier):
    """A JSON:API resource identifier for a coach."""

    type: Literal["coaches"] = "coaches"
