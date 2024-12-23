"""Module for testing the common JSON:API schemas."""

import json
from typing import Any

from deepdiff import DeepDiff

from kwai.api.v1.schemas import CountryDocument
from kwai.modules.club.domain.country import CountryEntity


def test_create_country_document(
    country: CountryEntity, expected_country_json: dict[str, Any]
):
    """Test the creation of a document with a Country resource."""
    country_document = CountryDocument.create(country)
    json_resource = json.loads(country_document.json())

    diff = DeepDiff(json_resource, expected_country_json, ignore_order=True)
    assert not diff, f"JSON structure is not as expected: {diff}"
