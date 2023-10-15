"""Module for testing the news endpoints."""
from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from kwai.modules.portal.applications.application import ApplicationEntity
from kwai.modules.portal.news.news_item import NewsItemEntity

pytestmark = pytest.mark.api


def _find(resource_list: list[dict[str, Any]], id_: str):
    """Search for a resource with the given id."""
    for resource in resource_list:
        if resource["id"] == id_:
            return resource
    return None


def test_get_news_items(client: TestClient):
    """Test /api/v1/news_items."""
    response = client.get("/api/v1/news_items")
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert "meta" in json, "There should be a meta object in the response"
    assert json["meta"]["limit"] == 10, "The limit should be 10"
    assert "data" in json, "There should be a data list in the response"


def test_get_news_item(client: TestClient, news_item_entity: NewsItemEntity):
    """Test /api/v1/news_items/{news_item_entity.id}."""
    response = client.get(f"/api/v1/news_items/{news_item_entity.id}")
    json = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(json["data"]) > 0, "There should be at least one news item."

    json = response.json()
    assert "data" in json, "There should be data in the response"

    training_resource = json["data"]
    assert (
        training_resource is not None
    ), f"News item with id {news_item_entity.id} should exist"


def test_create_news_item(secure_client: TestClient, application: ApplicationEntity):
    """Test POST /api/v1/news_items."""
    payload = {
        "data": {
            "type": "news_items",
            "attributes": {
                "texts": [
                    {
                        "locale": "en",
                        "format": "md",
                        "title": "Test New Website",
                        "summary": "Testing the new website",
                    }
                ],
                "enabled": True,
                "publish_date": "2023-01-02 12:00:00",
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
    response = secure_client.post("/api/v1/news_items", json=payload)
    assert response.status_code == status.HTTP_201_CREATED, response.json()


def test_update_news_item(
    secure_client: TestClient,
    news_item_entity: NewsItemEntity,
    application: ApplicationEntity,
):
    """Test PATCH /api/v1/news_items."""
    payload = {
        "data": {
            "type": "news_items",
            "id": str(news_item_entity.id),
            "attributes": {
                "texts": [
                    {
                        "locale": "en",
                        "format": "md",
                        "title": "Test New Website",
                        "summary": "Testing the new website (update)",
                    }
                ],
                "enabled": True,
                "publish_date": "2023-01-02 12:00:00",
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
    response = secure_client.patch(
        f"/api/v1/news_items/{news_item_entity.id}", json=payload
    )
    assert response.status_code == status.HTTP_201_CREATED, response.json()


def test_delete_news_item(secure_client: TestClient, news_item_entity: NewsItemEntity):
    """Test DELETE /api/v1/news_items."""
    response = secure_client.delete(f"/api/v1/news_items/{news_item_entity.id}")
    assert response.status_code == status.HTTP_200_OK, response.json()
