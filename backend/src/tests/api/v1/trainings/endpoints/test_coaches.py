"""Module for testing the training/coaches endpoint."""

import pytest
from fastapi import status
from fastapi.testclient import TestClient

pytestmark = pytest.mark.api


def test_get_coaches(client: TestClient):
    """Test get coaches api."""
    response = client.get("/api/v1/trainings/coaches")
    assert response.status_code == status.HTTP_200_OK
