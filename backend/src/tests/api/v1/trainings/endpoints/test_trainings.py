"""Module for testing the trainings endpoints."""
import pytest
from fastapi import status
from fastapi.testclient import TestClient

pytestmark = pytest.mark.api


def test_get_trainings(client: TestClient):
    """Test get trainings api."""
    response = client.get("/api/v1/trainings")
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert "meta" in json, "There should be a meta object in the response"
    assert "data" in json, "There should be a data list in the response"


def test_get_trainings_filter_year_month(client: TestClient):
    """Test get trainings api with filter on year/month."""
    response = client.get(
        "/api/v1/trainings", params={"filter[year]": 2022, "filter[month]": 1}
    )
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert "meta" in json, "There should be a meta object in the response"
    assert "data" in json, "There should be a data list in the response"


def test_get_trainings_filter_start_end(client: TestClient):
    """Test get trainings api with a filter on start and end date."""
    response = client.get(
        "/api/v1/trainings",
        params={
            "filter[start]": "2022-01-01 00:00:00",
            "filter[end]": "2022-01-31 23:59:59",
        },
    )
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert "meta" in json, "There should be a meta object in the response"
    assert "data" in json, "There should be a data list in the response"
