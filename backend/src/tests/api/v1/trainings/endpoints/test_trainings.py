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


def test_get_trainings_filter_coach(client: TestClient):
    """Test get trainings api with a filter for a coach."""
    response = client.get(
        "/api/v1/trainings",
        params={"filter[coach]": "1"},
    )
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

    json = response.json()
    if response.status_code == status.HTTP_200_OK:
        assert "meta" in json, "There should be a meta object in the response"
        assert "data" in json, "There should be a data list in the response"
    else:
        assert "detail" in json


def test_get_trainings_filter_active(client: TestClient):
    """Test get trainings api with a filter for active trainings."""
    response = client.get(
        "/api/v1/trainings",
        params={"filter[active]": "false"},
    )
    assert response.status_code in [status.HTTP_200_OK]

    json = response.json()
    assert "meta" in json, "There should be a meta object in the response"
    assert "data" in json, "There should be a data list in the response"


def test_get_trainings_filter_definition(client: TestClient):
    """Test get trainings api with a filter for a definition."""
    response = client.get(
        "/api/v1/trainings",
        params={"filter[definition]": "1"},
    )
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

    json = response.json()
    if response.status_code == status.HTTP_200_OK:
        assert "meta" in json, "There should be a meta object in the response"
        assert "data" in json, "There should be a data list in the response"
    else:
        assert "detail" in json


def test_get_training(client: TestClient):
    """Test /api/v1/training/{training_id}."""
    response = client.get("/api/v1/trainings/1")
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

    json = response.json()
    if response.status_code == status.HTTP_200_OK:
        assert "data" in json, "There should be a data list in the response"
    else:
        assert "detail" in json


def test_create_training(secure_client: TestClient):
    """Test POST /api/v1/training."""
    payload = {
        "data": {
            "type": "trainings",
            "attributes": {
                "content": [
                    {
                        "locale": "en",
                        "format": "md",
                        "title": "U13 Training",
                        "summary": "Training for U13",
                    }
                ],
                "start_date": "2023-02-02 19:00:00",
                "end_date": "2023-02-02 20:00:00",
                "active": True,
                "cancelled": False,
                "location": "",
                "remark": "",
            },
            "relationships": {"coaches": {"data": []}, "teams": {"data": []}},
        }
    }
    response = secure_client.post("/api/v1/trainings", json=payload)
    assert response.status_code == status.HTTP_201_CREATED, response.json()


def test_create_training_with_coaches(secure_client: TestClient):
    """Test POST /api/v1/training with coaches."""
    payload = {
        "data": {
            "type": "trainings",
            "attributes": {
                "content": [
                    {
                        "locale": "en",
                        "format": "md",
                        "title": "U13 Training",
                        "summary": "Training for U13",
                    }
                ],
                "start_date": "2023-02-02 19:00:00",
                "end_date": "2023-02-02 20:00:00",
                "active": True,
                "cancelled": False,
                "location": "",
                "remark": "",
            },
            "relationships": {
                "coaches": {"data": [{"type": "training_coaches", "id": "1"}]},
                "teams": {"data": []},
            },
        }
    }
    response = secure_client.post("/api/v1/trainings", json=payload)
    assert response.status_code == status.HTTP_201_CREATED, response.json()


def test_create_training_with_teams(secure_client: TestClient):
    """Test POST /api/v1/training with teams."""
    payload = {
        "data": {
            "type": "trainings",
            "attributes": {
                "content": [
                    {
                        "locale": "en",
                        "format": "md",
                        "title": "U13 Training",
                        "summary": "Training for U13",
                    }
                ],
                "start_date": "2023-02-02 19:00:00",
                "end_date": "2023-02-02 20:00:00",
                "active": True,
                "cancelled": False,
                "location": "",
                "remark": "",
            },
            "relationships": {
                "coaches": {"data": []},
                "teams": {"data": [{"type": "teams", "id": "1"}]},
            },
        }
    }
    response = secure_client.post("/api/v1/trainings", json=payload)
    assert response.status_code == status.HTTP_201_CREATED, response.json()
