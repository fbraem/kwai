"""Module that defines all JSON:API resource identifiers for the club API."""

from typing import Literal

from kwai.core.json_api import ResourceIdentifier


class MemberResourceIdentifier(ResourceIdentifier):
    """A JSON:API resource identifier for a member."""

    type: Literal["members"] = "members"


class PersonResourceIdentifier(ResourceIdentifier):
    """A JSON:API resource identifier for a person."""

    type: Literal["persons"] = "persons"


class ContactResourceIdentifier(ResourceIdentifier):
    """A JSON:API resource identifier for a contact."""

    type: Literal["contacts"] = "contacts"


class UploadResourceIdentifier(ResourceIdentifier):
    """A JSON:API resource identifier for a upload."""

    type: Literal["uploads"] = "uploads"
