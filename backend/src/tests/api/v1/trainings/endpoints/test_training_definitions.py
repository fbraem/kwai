"""Module for testing the training_definitions end point."""
import pytest
from fastapi import status
from fastapi.testclient import TestClient

pytestmark = pytest.mark.api


def test_get_training_definitions(client: TestClient):
    """Test get training definitions api."""
    response = client.get("/api/v1/training_definitions")
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert "meta" in json, "There should be a meta object in the response"
    assert "data" in json, "There should be a data list in the response"


def test_get_training_definition(client: TestClient):
    """Test get training definition api."""
    response = client.get("/api/v1/training_definitions/1")
    assert response.status_code in (status.HTTP_200_OK, status.HTTP_404_NOT_FOUND)

    json = response.json()
    if response.status_code == status.HTTP_200_OK:
        assert "data" in json, "There should be a data list in the response"
    else:
        assert "detail" in json


def test_delete_training_definition(client: TestClient):
    """Test delete training definition."""
    response = client.delete(f"")
    assert response.status_code == status.HTTP_200_OK
