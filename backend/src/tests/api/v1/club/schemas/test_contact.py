"""Module for testing the contact JSON:API resource."""

import json
from typing import Any

from deepdiff import DeepDiff

from kwai.api.v1.club.schemas.contact import ContactDocument
from kwai.modules.club.domain.contact import ContactEntity


def test_create_contact_document(
    contact: ContactEntity, expected_contact_json: dict[str, Any]
):
    """Test the creation of a contact document."""
    contact_document = ContactDocument.create(contact)
    json_resource = json.loads(contact_document.json())

    diff = DeepDiff(json_resource, expected_contact_json, ignore_order=True)
    assert not diff, f"JSON structure is not as expected: {diff}"
