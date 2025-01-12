"""Module for testing the trainings/team API."""

import pytest

from fastapi import status
from fastapi.testclient import TestClient


pytestmark = pytest.mark.api


def test_get_teams(client: TestClient):
    """Test get trainings teams api."""
    response = client.get("/api/v1/trainings/teams")
    assert response.status_code == status.HTTP_200_OK
