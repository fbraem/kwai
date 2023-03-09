"""Test the endpoint users."""
import pytest
from fastapi import status
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration


def test_get_user_invitations(secure_client: TestClient):
    """Test GET users/invitations."""
    response = secure_client.get("api/v1/auth/users/invitations")
    assert response.status_code == status.HTTP_200_OK
