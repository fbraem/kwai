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
    assert (
        training_definition_resource["type"] == "training_definitions"
    ), "The resource should have the type 'training_definitions'."
    assert (
        training_definition_resource is not None
    ), f"Training with id {training_definition_entity.id} should exist"


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


def test_delete_training_definition(
    secure_client: TestClient, training_definition_entity: TrainingDefinitionEntity
):
    """Test delete training definition."""
    response = secure_client.delete(
        f"/api/v1/training_definitions/{training_definition_entity.id}"
    )
    assert response.status_code == status.HTTP_200_OK
