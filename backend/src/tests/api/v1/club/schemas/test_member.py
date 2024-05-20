"""Module for testing the member JSON:API resource."""

import json
from typing import Any

import pytest
from deepdiff import DeepDiff
from kwai.api.v1.club.schemas.member import MemberDocument
from kwai.core.domain.value_objects.date import Date
from kwai.modules.club.domain.member import MemberEntity, MemberIdentifier
from kwai.modules.club.domain.person import PersonEntity
from kwai.modules.club.domain.value_objects import License


@pytest.fixture
def member(person: PersonEntity) -> MemberEntity:
    """A fixture for a member entity."""
    return MemberEntity(
        id_=MemberIdentifier(1),
        license=License(number="1234567890", end_date=Date.today().add(years=1)),
        person=person,
    )


@pytest.fixture
def expected_member_json(
    member: MemberEntity, expected_person_json: dict[str, Any]
) -> dict[str, Any]:
    """A fixture for a JSON:API resource of a member."""
    return {
        "data": {
            "id": str(member.uuid),
            "type": "members",
            "attributes": {
                "license_number": "1234567890",
                "license_end_date": str(member.license.end_date),
                "remark": "",
                "active": True,
                "competition": False,
            },
            "meta": {
                "created_at": str(member.traceable_time.created_at),
                "updated_at": str(member.traceable_time.updated_at),
            },
            "relationships": {
                "person": {
                    "data": {
                        "id": expected_person_json["data"]["id"],
                        "type": expected_person_json["data"]["type"],
                    }
                }
            },
        },
        "included": [expected_person_json["data"], *expected_person_json["included"]],
    }


def test_create_member_document(
    member: MemberEntity, expected_member_json: dict[str, Any]
):
    """Test the creation of a JSON:API document for a Member resource."""
    member_document = MemberDocument.create(member)
    json_resource = json.loads(member_document.json())

    diff = DeepDiff(json_resource, expected_member_json, ignore_order=True)
    assert not diff, f"JSON structure is not expected: {diff}"
