"""Module that defines fixtures for the api tests."""

import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from kwai.api.app import create_api
from kwai.core.settings import get_settings
from kwai.modules.identity.users.user_account import UserAccountEntity


@pytest.fixture(scope="module")
def client() -> TestClient:
    """Get an HTTP client."""
    app = FastAPI(title="kwai API -- TEST")
    app.mount("/api", create_api(get_settings()))
    return TestClient(app)


@pytest.fixture(scope="module")
def secure_client(client: TestClient, user_account: UserAccountEntity) -> TestClient:
    """Return a test client that is logged-in."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": str(user_account.user.email), "password": "Nage-waza/1882"},
    )
    client.cookies.set("access_token", response.cookies["access_token"])
    client.cookies.set("refresh_token", response.cookies["refresh_token"])

    return client
