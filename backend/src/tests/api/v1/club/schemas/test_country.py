"""Module for testing the country JSON:API resource."""

import json
from typing import Any

from deepdiff import DeepDiff

from kwai.api.v1.club.schemas.country import CountryDocument
from kwai.modules.club.members.value_objects import Country


def test_country_document(country: Country, expected_country_json: dict[str, Any]):
    """Test the creation of a document with a Country resource."""
    country_document = CountryDocument.create(country)
    json_resource = json.loads(country_document.json())

    diff = DeepDiff(json_resource, expected_country_json, ignore_order=True)
    assert not diff, f"JSON structure is not as expected: {diff}"
