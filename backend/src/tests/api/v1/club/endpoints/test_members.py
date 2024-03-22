"""Module for testing the members endpoint of the club API."""

import pytest
from fastapi import status
from fastapi.testclient import TestClient

pytestmark = pytest.mark.api


def test_get_members(secure_client: TestClient):
    """Test /api/v1/club/members."""
    response = secure_client.get("/api/v1/club/members")
    assert response.status_code == status.HTTP_200_OK
