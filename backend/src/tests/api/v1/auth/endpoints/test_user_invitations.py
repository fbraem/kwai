"""Test the endpoint users."""

import json

import pytest

from fastapi import status
from fastapi.testclient import TestClient

from kwai.core.db.database import Database
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    UserInvitationDbRepository,
)
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationRepository,
)


pytestmark = [pytest.mark.api, pytest.mark.db]


@pytest.fixture(scope="module")
def repo(database: Database) -> UserInvitationRepository:
    """Create the invitation repository."""
    return UserInvitationDbRepository(database)


@pytest.fixture(scope="module")
def invitation_data() -> list[str]:
    """Create array to capture the uuid created in test_create_user_invitation."""
    return []


@pytest.mark.mail
def test_create_user_invitation(secure_client: TestClient, invitation_data: list[str]):
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
    assert response.status_code == status.HTTP_201_CREATED, response.content

    invitation_data.append(response.json()["data"]["id"])


def test_get_user_invitations(secure_client: TestClient):
    """Test GET users/invitations."""
    response = secure_client.get("api/v1/auth/users/invitations")
    assert response.status_code == status.HTTP_200_OK


def test_get_user_invitation(
    secure_client: TestClient,
    invitation_data: list[str],
):
    """Test GET users/invitations/<uuid>."""
    if len(invitation_data) > 0:
        response = secure_client.get(
            f"api/v1/auth/users/invitations/{invitation_data[0]}"
        )
        assert response.status_code == status.HTTP_200_OK
    else:
        pytest.skip("Test skipped because there is no user invitation")


def test_delete_user_invitation(secure_client: TestClient, invitation_data: list[str]):
    """Test DELETE users/invitations/<uuid>."""
    if len(invitation_data) > 0:
        response = secure_client.delete(
            f"api/v1/auth/users/invitations/{invitation_data[0]}"
        )
        assert response.status_code == status.HTTP_200_OK
    else:
        pytest.skip("Test skipped because there is no user invitation")
