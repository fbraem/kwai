"""Module for testing the pages endpoint."""

from fastapi import status
from fastapi.testclient import TestClient

from kwai.modules.portal.applications.application import ApplicationEntity
from kwai.modules.portal.pages.page import PageEntity


def test_get_pages(client: TestClient):
    """Test GET /api/v1/pages."""
    response = client.get("/api/v1/pages")
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert "meta" in json, "There should be a meta object in the response"
    assert "data" in json, "There should be a data list in the response"


def test_get_page(client: TestClient, page_entity: PageEntity):
    """Test /api/v1/pages/{id}."""
    response = client.get(f"/api/v1/pages/{page_entity.id}")
    json = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(json["data"]) > 0, "There should be at least one page."

    json = response.json()
    assert "data" in json, "There should be data in the response"

    training_resource = json["data"]
    assert training_resource is not None, f"Page with id {page_entity.id} should exist"


def test_create_page(secure_client: TestClient, application: ApplicationEntity):
    """Test POST /api/v1/pages."""
    payload = {
        "data": {
            "type": "pages",
            "attributes": {
                "texts": [
                    {
                        "locale": "en",
                        "format": "md",
                        "title": "Test New Website",
                        "summary": "Testing the new website",
                        "original_summary": "Testing the new website",
                        "content": "Testing the new website content",
                        "original_content": "Testing the new website content",
                    }
                ],
                "enabled": True,
                "priority": 0,
                "remark": "",
            },
            "relationships": {
                "application": {
                    "data": {"type": "applications", "id": str(application.id)}
                }
            },
        },
    }
    response = secure_client.post("/api/v1/pages", json=payload)
    assert response.status_code == status.HTTP_201_CREATED, response.json()


def test_patch_page(
    secure_client: TestClient, page_entity: PageEntity, application: ApplicationEntity
):
    """Test PATCH /api/v1/pages."""
    payload = {
        "data": {
            "id": str(page_entity.id),
            "type": "pages",
            "attributes": {
                "texts": [
                    {
                        "locale": "en",
                        "format": "md",
                        "title": "Test New Website",
                        "summary": "Testing the new website (update)",
                        "original_summary": "Testing the new website (update)",
                        "content": "Testing the new website content (update)",
                        "original_content": "Testing the new website content (update)",
                    }
                ],
                "enabled": True,
                "priority": 0,
                "remark": "Updated",
            },
            "relationships": {
                "application": {
                    "data": {"type": "applications", "id": str(application.id)}
                }
            },
        },
    }
    response = secure_client.patch(f"/api/v1/pages/{page_entity.id}", json=payload)
    assert response.status_code == status.HTTP_200_OK, response.json()


def test_delete_page(secure_client: TestClient, page_entity: PageEntity):
    """Test DELETE /api/v1/pages."""
    response = secure_client.delete(f"/api/v1/pages/{page_entity.id}")
    assert response.status_code == status.HTTP_200_OK, response.json()
