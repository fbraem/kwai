"""Module for testing the trainings endpoints."""
import pytest
from fastapi import status
from fastapi.testclient import TestClient

pytestmark = pytest.mark.api


def test_get_trainings(client: TestClient):
    """Test get trainings api."""
    response = client.get("/api/v1/trainings")
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert "meta" in json, "There should be a meta object in the response"
    assert "data" in json, "There should be a data list in the response"
