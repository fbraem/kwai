"""Module for testing the schemas for the /api/v1/auth/authors endpoint."""

import json

import pytest

from deepdiff import DeepDiff

from kwai.api.v1.auth.authors.schemas import AuthorDocument, AuthorResource
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.portal.domain.author import AuthorEntity, AuthorIdentifier


@pytest.fixture
def author() -> AuthorEntity:
    """A fixture for an author entity."""
    return AuthorEntity(
        id=AuthorIdentifier(1),
        uuid=UniqueId.generate(),
        name="Jigoro Kano",
        remark="Test author",
    )


def test_author_schema(author):
    """Test creation of an Author JSON:API document."""
    author_document = AuthorDocument(data=AuthorResource.create(author))
    json_resource = json.loads(author_document.model_dump_json())

    expected_author_json = {
        "data": {
            "id": str(author.uuid),
            "type": "authors",
            "attributes": {
                "name": "Jigoro Kano",
                "remark": "Test author",
                "active": True,
            },
            "meta": {
                "created_at": str(author.traceable_time.created_at),
                "updated_at": None,
            },
        }
    }

    diff = DeepDiff(json_resource, expected_author_json)
    assert not diff, f"JSON structure is not as expected: {diff}"
