"""Test the endpoint users."""
import json

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.modules.identity.user_invitations.user_invitation import UserInvitationEntity
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    InvitationDbRepository,
)
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationRepository,
)
from kwai.modules.identity.users.user import UserEntity

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def repo(database: Database) -> UserInvitationRepository:
    """Fixture for creating the invitation repository."""
    return InvitationDbRepository(database)


@pytest.fixture(scope="module")
def user_invitation(
    repo: UserInvitationRepository, user: UserEntity
) -> UserInvitationEntity:
    """Fixture for a user invitation."""
    invitation = UserInvitationEntity(
        email=EmailAddress("ichiro.abe@kwai.com"),
        name=Name(first_name="Ichiro", last_name="Abe"),
        remark="Created with pytest",
        user=user,
    )
    yield repo.create(invitation)
    repo.delete(invitation)


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


def test_get_user_invitation(
    secure_client: TestClient, user_invitation: UserInvitationEntity
):
    """Test GET users/invitations/<uuid>"""
    response = secure_client.get(
        f"api/v1/auth/users/invitations/{user_invitation.uuid}"
    )
    assert response.status_code == status.HTTP_200_OK
