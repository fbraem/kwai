"""Module for testing the upload members endpoint of the club API."""

from pathlib import Path

import pytest
from fastapi import status
from fastapi.testclient import TestClient

pytestmark = pytest.mark.api


def test_import_members(secure_client: TestClient):
    """Test /api/v1/club/members/upload."""
    filename = Path(__file__).parent / "data" / "flemish_members_test.csv"

    with open(filename, "rb") as file_handle:
        response = secure_client.post(
            "/api/v1/club/members/upload", files={"member_file": file_handle}
        )
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert "data" in result, "There should be a 'members' property."
        assert len(result["data"]) == 2, "There should be 2 members uploaded."
