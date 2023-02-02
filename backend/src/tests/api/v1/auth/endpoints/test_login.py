"""Module for testing the auth endpoints login."""
import pytest
from fastapi import status
from fastapi.testclient import TestClient

from kwai.modules.identity.users.user_account import UserAccountEntity

pytestmark = pytest.mark.integration


def test_login(user_account: UserAccountEntity, client: TestClient):
    """Test the login api."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": str(user_account.user.email), "password": "Nage-waza/1882"},
    )
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert "access_token" in json
    assert "refresh_token" in json
    assert "expiration" in json


def test_login_with_unknown_user(client: TestClient):
    """Test the login api with an unknown email address."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "unknown@kwai.com", "password": "Nage-waza/1882"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_with_wrong_password(user_account: UserAccountEntity, client: TestClient):
    """Test the login api with a wrong password."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": str(user_account.user.email), "password": "Test/1234"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
