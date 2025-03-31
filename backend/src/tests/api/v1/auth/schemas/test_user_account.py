"""Module for testing the user invitation JSON:API resource."""

import json

from deepdiff import DeepDiff

from kwai.api.v1.auth.schemas.user_account import (
    UserAccountDocument,
    UserAccountResource,
)


def test_create_user_invitation_document(make_user_account):
    """Test creation of a user invitation JSON:API document."""
    user_account = make_user_account()
    user_account_document = UserAccountDocument(
        data=UserAccountResource.create(user_account)
    )
    json_resource = json.loads(user_account_document.model_dump_json())

    expected_user_account_json = {
        "data": {
            "id": str(user_account.user.uuid),
            "type": "user_accounts",
            "attributes": {
                "email": "jigoro.kano@kwai.com",
                "last_login": None,
                "last_unsuccessful_login": None,
                "revoked": False,
                "admin": False,
                "first_name": "Jigoro",
                "last_name": "Kano",
                "remark": "",
            },
        }
    }

    diff = DeepDiff(json_resource, expected_user_account_json, ignore_order=True)
    assert not diff, f"JSON structure is not as expected: {diff}"
