"""Module for testing the revoked_users endpoint."""

import json

import pytest

from fastapi import status


pytestmark = [pytest.mark.api, pytest.mark.db]


async def test_create_revoked_user(secure_client, make_user_account_in_db):
    """Test the POST revoke_user endpoint."""
    user_account = await make_user_account_in_db()
    data = {
        "data": {
            "type": "revoked_users",
            "id": str(user_account.user.uuid),
            "attributes": {
                "revoked": True,
            },
        }
    }
    response = secure_client.post(
        "/api/v1/auth/revoked_users", content=json.dumps(data)
    )
    assert response.status_code == status.HTTP_201_CREATED, response.text


async def test_delete_revoked_user(
    secure_client, make_user_account_in_db, make_user_account
):
    """Test the DELETE revoke_user endpoint."""
    user_account = await make_user_account_in_db(make_user_account(revoked=True))
    response = secure_client.delete(
        f"/api/v1/auth/revoked_users/{user_account.user.uuid}"
    )
    assert response.status_code == status.HTTP_200_OK, response.text
