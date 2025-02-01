"""Module for testing the revoked user JSON:API resource."""

import json

from deepdiff import DeepDiff

from kwai.api.v1.auth.schemas.revoked_user import RevokedUserDocument


def test_create_revoked_user_document(make_user_account):
    """Test creation of a user invitation JSON:API document."""
    user_account = make_user_account()
    user_account = user_account.revoke()
    revoked_user_document = RevokedUserDocument.create(user_account)
    json_resource = json.loads(revoked_user_document.model_dump_json())

    expected_revoked_user_json = {
        "data": {
            "id": str(user_account.user.uuid),
            "type": "revoked_users",
            "attributes": {"revoked": True},
        }
    }

    diff = DeepDiff(json_resource, expected_revoked_user_json, ignore_order=True)
    assert not diff, f"JSON structure is not as expected: {diff}"
