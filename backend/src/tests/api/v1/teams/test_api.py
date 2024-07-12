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
