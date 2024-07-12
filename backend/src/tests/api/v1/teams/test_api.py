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
