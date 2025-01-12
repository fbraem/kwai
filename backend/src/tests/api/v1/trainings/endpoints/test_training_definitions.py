"""Module for testing the training_definitions end point."""

from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from kwai.modules.training.trainings.training_definition import TrainingDefinitionEntity

pytestmark = pytest.mark.api


def _find(resource_list: list[dict[str, Any]], id_: str):
    """Search for a resource with the given id."""
    for resource in resource_list:
        if resource["id"] == id_:
            return resource
    return None


def test_get_training_definitions(
    client: TestClient, training_definition_entity: TrainingDefinitionEntity
):
    """Test get training definitions api."""
    response = client.get("/api/v1/training_definitions")
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert "meta" in json, "There should be a meta object in the response"
    assert "data" in json, "There should be a data list in the response"
    assert len(json["data"]) > 0, "There should be at least one training"

    training_definition_resource = _find(
        json["data"], str(training_definition_entity.id)
    )
    assert training_definition_resource["type"] == "training_definitions", (
        "The resource should have the type 'training_definitions'."
    )
    assert training_definition_resource is not None, (
        f"Training with id {training_definition_entity.id} should exist"
    )


def test_get_training_definition(
    client: TestClient, training_definition_entity: TrainingDefinitionEntity
):
    """Test get training definition api."""
    response = client.get(
        f"/api/v1/training_definitions/{training_definition_entity.id}"
    )
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert "data" in json, "There should be a data list in the response"


def test_create_training_definition(secure_client: TestClient):
    """Test create training definition."""
    payload = {
        "data": {
            "type": "training_definitions",
            "attributes": {
                "name": "U9 Training",
                "description": "Monday training for U9",
                "weekday": 1,
                "start_time": "19:00",
                "end_time": "20:00",
                "timezone": "Europe/Brussels",
                "active": True,
                "location": "Sports Hall",
            },
            "relationships": {"data": {}},
        }
    }
    response = secure_client.post("/api/v1/training_definitions", json=payload)
    assert response.status_code == status.HTTP_201_CREATED, response.json()


def test_update_training_definition(
    secure_client: TestClient, training_definition_entity: TrainingDefinitionEntity
):
    """Test update training definition."""
    payload = {
        "data": {
            "type": "training_definitions",
            "attributes": {
                "name": "U9 Training",
                "description": "Monday training for U9",
                "weekday": 1,
                "start_time": "19:00",
                "end_time": "20:00",
                "timezone": "Europe/Brussels",
                "active": True,
                "location": "Sports Hall",
                "remark": "Updated with API",
            },
            "relationships": {"data": {}},
        }
    }
    response = secure_client.patch(
        f"/api/v1/training_definitions/{training_definition_entity.id}", json=payload
    )
    assert response.status_code == status.HTTP_200_OK, response.json()


def test_delete_training_definition(
    secure_client: TestClient, training_definition_entity: TrainingDefinitionEntity
):
    """Test delete training definition."""
    response = secure_client.delete(
        f"/api/v1/training_definitions/{training_definition_entity.id}"
    )
    assert response.status_code == status.HTTP_200_OK


def test_get_trainings(
    client: TestClient, training_definition_entity: TrainingDefinitionEntity
):
    """Test get trainings from a training definition."""
    response = client.get(
        f"/api/v1/training_definitions/{training_definition_entity.id}/trainings"
    )
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert "meta" in json, "There should be a meta object in the response"
    assert "data" in json, "There should be a data list in the response"
