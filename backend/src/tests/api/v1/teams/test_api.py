"""Module for testing the teams API."""

import pytest
from fastapi import status
from fastapi.testclient import TestClient

pytestmark = pytest.mark.api


async def test_get_team(client: TestClient, make_team_in_db):
    """Test /api/v1/teams endpoint for getting a team."""
    team = await make_team_in_db()
    response = client.get(f"/api/v1/teams/{team.id}")
    assert response.status_code == status.HTTP_200_OK


async def test_get_teams(client: TestClient, make_team_in_db):
    """Test /api/v1/teams endpoint for getting all teams."""
    await make_team_in_db()
    response = client.get("/api/v1/teams")
    assert response.status_code == status.HTTP_200_OK


async def test_delete_team(secure_client: TestClient, make_team_in_db):
    """Test /api/v1/teams endpoint for deleting a team."""
    team = await make_team_in_db()
    response = secure_client.delete(f"/api/v1/teams/{team.id}")
    assert response.status_code == status.HTTP_200_OK


async def test_create_team(secure_client: TestClient, make_team):
    """Test /api/v1/teams endpoint for creating a team."""
    team = make_team()
    payload = {
        "data": {
            "type": "teams",
            "attributes": {
                "name": team.name,
                "active": team.is_active,
                "remark": team.remark,
            },
        }
    }
    response = secure_client.post("/api/v1/teams", json=payload)
    assert response.status_code == status.HTTP_201_CREATED


async def test_update_team(secure_client: TestClient, make_team_in_db):
    """Test /api/v1/teams endpoint for updating a team."""
    team = await make_team_in_db()
    payload = {
        "data": {
            "id": str(team.id),
            "type": "teams",
            "attributes": {
                "name": team.name,
                "active": team.is_active,
                "remark": "This is a test",
            },
        }
    }
    response = secure_client.patch(f"/api/v1/teams/{team.id}", json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert (
        response.json()["data"]["attributes"]["remark"] == "This is a test"
    ), "The team should be updated."


async def test_get_members(
    secure_client: TestClient, make_team_in_db, make_member_in_db
):
    """Test /api/v1/teams/members endpoint for getting members."""
    team = await make_team_in_db()
    await make_member_in_db()
    response = secure_client.get(f"/api/v1/teams/members?filter[team]=noteq:{team.id}")
    assert response.status_code == status.HTTP_200_OK


async def test_get_team_members(
    secure_client: TestClient, make_team_in_db, make_team_member_in_db
):
    """Test /api/v1/teams/<id>/members endpoint for getting a team's members."""
    team = await make_team_in_db()
    await make_team_member_in_db(team=team)
    response = secure_client.get(f"/api/v1/teams/{team.id}/members")
    assert response.status_code == status.HTTP_200_OK


async def test_create_team_member(
    secure_client: TestClient, make_team_in_db, make_member_in_db
):
    """Test /api/v1/teams/<id>/members endpoint for creating a team's member."""
    team = await make_team_in_db()
    member = await make_member_in_db()
    payload = {
        "data": {
            "type": "team_members",
            "id": str(member.uuid),
            "attributes": {
                "active": True,
                "first_name": member.person.name.first_name,
                "last_name": member.person.name.last_name,
                "license_number": member.license.number,
                "license_end_date": str(member.license.end_date),
                "gender": member.person.gender.value,
                "birthdate": str(member.person.birthdate),
            },
            "relationships": {
                "nationality": {
                    "data": {
                        "type": "countries",
                        "id": str(member.person.nationality.id),
                    }
                }
            },
        }
    }
    response = secure_client.post(f"/api/v1/teams/{team.id}/members", json=payload)
    assert response.status_code == status.HTTP_201_CREATED, response.json()
