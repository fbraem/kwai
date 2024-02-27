"""Module for testing the members endpoint of the club API."""

from pathlib import Path

import pytest
from fastapi import status
from fastapi.testclient import TestClient

pytestmark = pytest.mark.api


def test_import_members(secure_client: TestClient):
    """Test /api/v1/club/members."""
    filename = Path(__file__).parent / "data" / "flemish_members_test.csv"

    response = secure_client.post(
        "/api/v1/club/members/upload", files={"member_file": str(filename)}
    )
    assert response.status_code == status.HTTP_200_OK
