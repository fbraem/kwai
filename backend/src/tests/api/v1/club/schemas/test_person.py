"""Module for testing the person JSON:API schema."""

import json
from typing import Any

from deepdiff import DeepDiff

from kwai.api.v1.club.schemas.person import PersonDocument
from kwai.modules.club.members.person import PersonEntity


def test_create_person_document(
    person: PersonEntity, expected_person_json: dict[str, Any]
):
    """Test the creation of a person document."""
    person_document = PersonDocument.create(person)
    json_resource = json.loads(person_document.json())

    diff = DeepDiff(json_resource, expected_person_json, ignore_order=True)
    assert not diff, f"JSON structure is not as expected: {diff}"
