"""Module for testing the user invitation JSON:API resource."""

import json

import pytest
from deepdiff import DeepDiff

from kwai.api.v1.auth.schemas.user_invitation import UserInvitationDocument
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.modules.identity.user_invitations.user_invitation import (
    UserInvitationEntity,
    UserInvitationIdentifier,
)
from kwai.modules.identity.users.user import UserEntity, UserIdentifier


@pytest.fixture
def user() -> UserEntity:
    """A fixture for a user entity."""
    return UserEntity(
        id_=UserIdentifier(1),
        email=EmailAddress("jigoro.kano@kwai.com"),
        name=Name(first_name="Jigoro", last_name="Kano"),
    )


@pytest.fixture
def user_invitation(user: UserEntity):
    """A fixture for a user invitation entity."""
    return UserInvitationEntity(
        id=UserInvitationIdentifier(1),
        email=EmailAddress("ichiro.abe@kwai.com"),
        name=Name(first_name="Ichiro", last_name="Abe"),
        user=user,
    )


def test_create_user_invitation_document(user_invitation: UserInvitationEntity):
    """Test creation of a user invitation JSON:API document."""
    user_invitation_document = UserInvitationDocument.create(user_invitation)
    json_resource = json.loads(user_invitation_document.json())

    expected_user_invitation_json = {
        "data": {
            "id": str(user_invitation.uuid),
            "type": "user_invitations",
            "attributes": {
                "email": "ichiro.abe@kwai.com",
                "first_name": "Ichiro",
                "last_name": "Abe",
                "remark": "",
                "expired_at": str(user_invitation.expired_at),
                "confirmed_at": None,
            },
        }
    }

    diff = DeepDiff(json_resource, expected_user_invitation_json, ignore_order=True)
    assert not diff, f"JSON structure is not as expected: {diff}"
