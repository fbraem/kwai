"""Module that defines fixtures for the api tests."""

import pytest
from fastapi.testclient import TestClient
from kwai.api.app import create_app
from kwai.core.settings import get_settings
from kwai.modules.identity.users.user_account import UserAccountEntity


@pytest.fixture(scope="module")
def client() -> TestClient:
    """Get an HTTP client."""
    app = create_app(get_settings())
    return TestClient(app)


@pytest.fixture(scope="module")
def secure_client(client: TestClient, user_account: UserAccountEntity) -> TestClient:
    """Return a test client that is logged-in."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": str(user_account.user.email), "password": "Nage-waza/1882"},
    )
    access_token = response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {access_token}"

    return client
