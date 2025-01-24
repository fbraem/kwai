"""Module that defines all JSON:API resource identifiers for the auth API."""

from typing import Literal

from kwai.core.json_api import ResourceIdentifier


class UserAccountResourceIdentifier(ResourceIdentifier):
    """A JSON:API resource identifier for a user account."""

    type: Literal["user_accounts"] = "user_accounts"
