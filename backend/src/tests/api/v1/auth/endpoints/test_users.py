"""Test the endpoint users."""
import json

import pytest
from fastapi import status
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration


@pytest.mark.asyncio
async def test_create_user_invitation(secure_client: TestClient):
    """Test POST users/invitations."""
    data = {
        "data": {
            "type": "user_invitations",
            "attributes": {
                "email": "ichiro.abe@kwai.com",
                "first_name": "Ichiro",
                "last_name": "Abe",
                "remark": "Invitation created in test_create_user_invitation",
            },
        }
    }
    response = secure_client.post(
        "api/v1/auth/users/invitations", content=json.dumps(data)
    )
    assert response.status_code == status.HTTP_200_OK


def test_get_user_invitations(secure_client: TestClient):
    """Test GET users/invitations."""
    response = secure_client.get("api/v1/auth/users/invitations")
    assert response.status_code == status.HTTP_200_OK
