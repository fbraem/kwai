"""Module for testing teams schemas."""

import json
from typing import Any

import pytest
from deepdiff import DeepDiff
from kwai.api.v1.teams.schemas import TeamDocument, TeamMemberDocument
from kwai.core.domain.value_objects.date import Date
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.club.domain.value_objects import Birthdate, Gender, License
from kwai.modules.teams.domain.team import TeamEntity, TeamIdentifier
from kwai.modules.teams.domain.team_member import TeamMemberEntity, TeamMemberIdentifier

from tests.fixtures.club.countries import *  # noqa


@pytest.fixture
def team_member(country_japan) -> TeamMemberEntity:
    """A fixture for a team member."""
    return TeamMemberEntity(
        id_=TeamMemberIdentifier(1),
        name=Name(first_name="Jigoro", last_name="Kano"),
        uuid=UniqueId.generate(),
        license=License(number="1234", end_date=Date.today().add(years=1)),
        birthdate=Birthdate(Date.create(year=1860, month=10, day=28)),
        gender=Gender.MALE,
        nationality=country_japan,
    )


@pytest.fixture
def expected_team_member_json(team_member: TeamMemberEntity) -> dict[str, Any]:
    """A fixture for a JSON:API resource of a team member."""
    return {
        "data": {
            "id": str(team_member.uuid),
            "type": "members",
            "attributes": {
                "first_name": "Jigoro",
                "last_name": "Kano",
                "gender": team_member.gender.value,
                "birthdate": str(team_member.birthdate),
                "license_number": team_member.license.number,
                "license_end_date": str(team_member.license.end_date),
            },
            "relationships": {
                "nationality": {
                    "data": {
                        "id": str(team_member.nationality.id),
                        "type": "countries",
                    }
                }
            },
        },
        "included": [
            {
                "id": str(team_member.nationality.id),
                "type": "countries",
                "attributes": {"iso_2": "JP", "iso_3": "JPN", "name": "Japan"},
            }
        ],
    }


def test_create_team_member_document(
    team_member: TeamMemberEntity, expected_team_member_json: dict[str, Any]
):
    """Test the creation of a JSON:API document for a team member resource."""
    team_member_document = TeamMemberDocument.create(team_member)
    json_resource = json.loads(team_member_document.json())

    diff = DeepDiff(json_resource, expected_team_member_json, ignore_order=True)
    assert not diff, f"JSON structure is not expected:{diff}"


@pytest.fixture
def team(team_member: TeamMemberEntity) -> TeamEntity:
    """A fixture for a team entity."""
    return TeamEntity(
        id_=TeamIdentifier(1),
        name="U11",
        members=[team_member],
    )


@pytest.fixture
def expected_team_json(team: TeamEntity, expected_team_member_json) -> dict[str, Any]:
    """A fixture for a JSON:API resource of a team."""
    return {
        "data": {
            "id": "1",
            "type": "teams",
            "attributes": {"name": "U11", "remark": "", "active": True},
            "relationships": {
                "members": {
                    "data": [
                        {
                            "id": expected_team_member_json["data"]["id"],
                            "type": expected_team_member_json["data"]["type"],
                        }
                    ]
                }
            },
        },
        "included": [
            expected_team_member_json["data"],
            *expected_team_member_json["included"],
        ],
    }


def test_create_team_document(team: TeamEntity, expected_team_json: dict[str, Any]):
    """Test the creation of a JSON:API document for a team entity."""
    team_document = TeamDocument.create(team)
    json_resource = json.loads(team_document.json())

    diff = DeepDiff(json_resource, expected_team_json, ignore_order=True)
    assert not diff, f"JSON structure is not expected:{diff}"