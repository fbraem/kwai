"""Module for testing the auth endpoints login."""

import pytest

from fastapi import status
from fastapi.testclient import TestClient

from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.modules.identity.user_recoveries.user_recovery import UserRecoveryEntity
from kwai.modules.identity.user_recoveries.user_recovery_db_repository import (
    UserRecoveryDbRepository,
)
from kwai.modules.identity.users.user_account import UserAccountEntity


pytestmark = [pytest.mark.api, pytest.mark.db]


def test_login(client: TestClient, user_account: UserAccountEntity):
    """Test the login api."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": str(user_account.user.email), "password": "Nage-waza/1882"},
    )
    assert response.status_code == status.HTTP_200_OK


def test_login_with_unknown_user(client: TestClient):
    """Test the login api with an unknown email address."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "unknown@kwai.com", "password": "Nage-waza/1882"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_with_wrong_password(client: TestClient, user_account: UserAccountEntity):
    """Test the login api with a wrong password."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": str(user_account.user.email), "password": "Test/1234"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_renew_access_token(secure_client: TestClient, user_account: UserAccountEntity):
    """Test the renewal of an access token."""
    response = secure_client.post("/api/v1/auth/access_token")
    secure_client.cookies.set("access_token", response.cookies["access_token"])
    secure_client.cookies.set("refresh_token", response.cookies["refresh_token"])

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.mail
def test_recover_user(client: TestClient, user_account: UserAccountEntity):
    """Test the recover user api."""
    response = client.post(
        "/api/v1/auth/recover", data={"email": str(user_account.user.email)}
    )
    assert response.status_code == status.HTTP_200_OK


def test_recover_unknown_user(client: TestClient):
    """Test the recover user api with an unknown user."""
    response = client.post("/api/v1/auth/recover", data={"email": "unknown@kwai.com"})
    # A wrong user also results in http status code 200.
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.mail
async def test_reset_password(
    client: TestClient, make_user_account_in_db, database: Database
):
    """Test the reset password api."""
    user_recovery = UserRecoveryEntity(
        expiration=Timestamp.create_with_delta(hours=2),
        user=await make_user_account_in_db(),
    )
    async with UnitOfWork(database):
        user_recovery = await UserRecoveryDbRepository(database).create(user_recovery)

    response = client.post(
        "/api/v1/auth/reset",
        data={"uuid": str(user_recovery.uuid), "password": "Nage-waza/1882"},
    )
    assert response.status_code == status.HTTP_200_OK


def test_logout(secure_client: TestClient, user_account: UserAccountEntity):
    """Test the logout api."""
    response = secure_client.post("/api/v1/auth/logout")
    assert response.status_code == status.HTTP_200_OK, response.text
