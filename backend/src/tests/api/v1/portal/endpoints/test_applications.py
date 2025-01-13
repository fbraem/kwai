"""Module for testing the portal applications endpoints."""

import pytest

from fastapi import status
from fastapi.testclient import TestClient

from kwai.core.db.database import Database
from kwai.modules.portal.applications.application import ApplicationEntity
from kwai.modules.portal.applications.application_db_repository import (
    ApplicationDbRepository,
)


pytestmark = pytest.mark.api


@pytest.fixture(scope="module")
async def application(database: Database) -> ApplicationEntity:
    """Fixture for an application."""
    repo = ApplicationDbRepository(database)
    application = ApplicationEntity(
        title="Test", name="test", short_description="An application used for testing"
    )
    application = await repo.create(application)

    yield application

    await repo.delete(application)


def test_get_applications(client: TestClient):
    """Test the get applications api."""
    response = client.get("/api/v1/portal/applications")
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert "meta" in json, "There should be a meta object in the response"
    assert "data" in json, "There should be a data list in the response"


def test_get_application(client: TestClient, application: ApplicationEntity):
    """Test the get application api."""
    response = client.get(f"/api/v1/portal/applications/{application.id}")
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert "data" in json, "There should be data in the response"


def test_get_application_not_found(client: TestClient):
    """Test if the get api responds with 404 when no application is found."""
    response = client.get("/api/v1/portal/applications/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_application(
    secure_client: TestClient,
    application: ApplicationEntity,
):
    """Test PATCH /api/v1/portal/applications."""
    payload = {
        "data": {
            "type": "applications",
            "id": str(application.id),
            "attributes": {
                "title": "Test",
                "name": "test",
                "short_description": "An application used for testing",
                "description": "",
                "weight": 0,
                "events": application.can_contain_events,
                "pages": application.can_contain_pages,
                "news": application.can_contain_news,
                "remark": "Updated",
            },
        },
    }
    response = secure_client.patch(
        f"/api/v1/portal/applications/{application.id}", json=payload
    )
    assert response.status_code == status.HTTP_200_OK, response.json()
