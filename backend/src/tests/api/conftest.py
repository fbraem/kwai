"""Module that defines fixtures for the api tests."""
import pytest
from fastapi.testclient import TestClient

from kwai.app import create_app
from kwai.core.settings import get_settings


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Get an HTTP client."""
    app = create_app(get_settings())
    return TestClient(app)
