"""Module for testing the members endpoint of the club API."""

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from kwai.core.domain.value_objects.unique_id import UniqueId

pytestmark = pytest.mark.api


def test_get_members(secure_client: TestClient):
    """Test /api/v1/club/members."""
    response = secure_client.get("/api/v1/club/members")
    assert response.status_code == status.HTTP_200_OK


def test_get_inactive_members(secure_client: TestClient):
    """Test /api/v1/club/members for inactive members."""
    response = secure_client.get(
        "/api/v1/club/members", params={"filter[enabled]": False}
    )
    assert response.status_code == status.HTTP_200_OK


def test_get_members_with_license_end_date(secure_client: TestClient):
    """Test /api/v1/club/members for members with given license end date."""
    response = secure_client.get(
        "/api/v1/club/members",
        params={"filter[license_end_month]": 1, "filter[license_end_year]": 2024},
    )
    assert response.status_code == status.HTTP_200_OK


def test_get_member_not_found(secure_client: TestClient):
    """Test /api/v1/club/members/{uuid} return not found."""
    uuid = str(UniqueId.generate())
    response = secure_client.get(f"/api/v1/club/members/{uuid}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
