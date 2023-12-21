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
