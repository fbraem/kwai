"""Module that defines common JSON:API resource identifiers."""

from typing import Literal

from kwai.core.json_api import ResourceIdentifier


class CountryResourceIdentifier(ResourceIdentifier):
    """A JSON:API resource identifier for a country."""

    type: Literal["countries"] = "countries"
