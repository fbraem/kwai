"""Module for testing the trainings endpoints."""
from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from kwai.modules.training.trainings.training import TrainingEntity

pytestmark = pytest.mark.api


def _find(resource_list: list[dict[str, Any]], id_: str):
    """Search for a resource with the given id."""
    for resource in resource_list:
        if resource["id"] == id_:
            return resource
    return None


def test_get_trainings(client: TestClient, training_entity: TrainingEntity):
    """Test get trainings api."""
    response = client.get("/api/v1/trainings")
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert "meta" in json, "There should be a meta object in the response"
    assert "data" in json, "There should be a data list in the response"
    assert len(json["data"]) > 0, "There should be at least one training"

    training_resource = _find(json["data"], str(training_entity.id))
    assert (
        training_resource is not None
    ), f"Training with id {training_entity.id} should exist"


def test_get_trainings_filter_year_month(
    client: TestClient, training_entity: TrainingEntity
):
    """Test get trainings api with filter on year/month."""
    response = client.get(
        "/api/v1/trainings", params={"filter[year]": 2023, "filter[month]": 1}
    )
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert "meta" in json, "There should be a meta object in the response"
    assert "data" in json, "There should be a data list in the response"
    assert len(json["data"]) > 0, "There should be at least one training"

    training_resource = _find(json["data"], str(training_entity.id))
    assert (
        training_resource is not None
    ), f"Training with id {training_entity.id} should exist"


def test_get_trainings_filter_start_end(
    client: TestClient, training_entity: TrainingEntity
):
    """Test get trainings api with a filter on start and end date."""
    response = client.get(
        "/api/v1/trainings",
        params={
            "filter[start]": "2023-01-01 00:00:00",
            "filter[end]": "2023-01-31 00:00:00",
        },
    )
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert "meta" in json, "There should be a meta object in the response"
    assert "data" in json, "There should be a data list in the response"
    assert len(json["data"]) > 0, "There should be at least one training"

    training_resource = _find(json["data"], str(training_entity.id))
    assert (
        training_resource is not None
    ), f"Training with id {training_entity.id} should exist"


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


def test_get_trainings_filter_active(
    client: TestClient, training_entity: TrainingEntity
):
    """Test get trainings api with a filter for active trainings."""
    response = client.get(
        "/api/v1/trainings",
        params={"filter[active]": "false"},
    )
    assert response.status_code in [status.HTTP_200_OK]

    json = response.json()
    assert "meta" in json, "There should be a meta object in the response"
    assert "data" in json, "There should be a data list in the response"
    assert len(json["data"]) > 0, "There should be at least one training"

    training_resource = _find(json["data"], str(training_entity.id))
    assert (
        training_resource is not None
    ), f"Training with id {training_entity.id} should exist"


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


def test_get_training(client: TestClient, training_entity: TrainingEntity):
    """Test /api/v1/trainings/{training_id}."""
    response = client.get(f"/api/v1/trainings/{training_entity.id}")
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert "data" in json, "There should be data in the response"

    training_resource = json["data"]
    assert (
        training_resource is not None
    ), f"Training with id {training_entity.id} should exist"


def test_create_training(secure_client: TestClient):
    """Test POST /api/v1/trainings."""
    payload = {
        "data": {
            "type": "trainings",
            "attributes": {
                "contents": [
                    {
                        "locale": "en",
                        "format": "md",
                        "title": "U13 Training",
                        "summary": "Training for U13",
                    }
                ],
                "coaches": [],
                "event": {
                    "start_date": "2023-02-02 19:00:00",
                    "end_date": "2023-02-02 20:00:00",
                    "active": True,
                    "cancelled": False,
                    "location": "",
                },
                "remark": "",
            },
            "relationships": {"coaches": {"data": []}, "teams": {"data": []}},
        }
    }
    response = secure_client.post("/api/v1/trainings", json=payload)
    assert response.status_code == status.HTTP_201_CREATED, response.json()


def test_create_training_with_coaches(secure_client: TestClient):
    """Test POST /api/v1/trainings with coaches."""
    payload = {
        "data": {
            "type": "trainings",
            "attributes": {
                "contents": [
                    {
                        "locale": "en",
                        "format": "md",
                        "title": "U13 Training",
                        "summary": "Training for U13",
                    }
                ],
                "coaches": [
                    {"id": "1", "head": False, "present": False, "payed": False}
                ],
                "event": {
                    "start_date": "2023-02-02 19:00:00",
                    "end_date": "2023-02-02 20:00:00",
                    "active": True,
                    "cancelled": False,
                    "location": "",
                },
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
    """Test POST /api/v1/trainings with teams."""
    payload = {
        "data": {
            "type": "trainings",
            "attributes": {
                "contents": [
                    {
                        "locale": "en",
                        "format": "md",
                        "title": "U13 Training",
                        "summary": "Training for U13",
                    }
                ],
                "coaches": [],
                "event": {
                    "start_date": "2023-02-02 19:00:00",
                    "end_date": "2023-02-02 20:00:00",
                    "active": True,
                    "cancelled": False,
                    "location": "",
                },
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


def test_update_training(secure_client: TestClient, training_entity: TrainingEntity):
    """Test PATCH /api/v1/trainings."""
    payload = {
        "data": {
            "type": "trainings",
            "id": str(training_entity.id),
            "attributes": {
                "contents": [
                    {
                        "locale": "en",
                        "format": "md",
                        "title": "U13 Training",
                        "summary": "Training for U13",
                    }
                ],
                "coaches": [],
                "event": {
                    "start_date": "2023-02-02 19:00:00",
                    "end_date": "2023-02-02 20:00:00",
                    "active": True,
                    "cancelled": False,
                    "location": "",
                },
                "remark": "Updated!",
            },
            "relationships": {
                "coaches": {"data": []},
                "teams": {"data": []},
            },
        }
    }
    response = secure_client.patch(
        f"/api/v1/trainings/{training_entity.id}", json=payload
    )
    assert response.status_code == status.HTTP_200_OK, response.json()


def test_delete_training(secure_client: TestClient, training_entity: TrainingEntity):
    """Test DELETE /api/v1/trainings/{id}."""
    response = secure_client.delete(f"/api/v1/trainings/{training_entity.id}")
    assert response.status_code == status.HTTP_200_OK, response.json()
