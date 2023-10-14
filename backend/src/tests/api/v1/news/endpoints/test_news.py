"""Module for testing the news endpoints."""
from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from kwai.modules.portal.news.news_item import NewsItemEntity

pytestmark = pytest.mark.api


def _find(resource_list: list[dict[str, Any]], id_: str):
    """Search for a resource with the given id."""
    for resource in resource_list:
        if resource["id"] == id_:
            return resource
    return None


def test_get_news_items(client: TestClient):
    """Test the get news stories api."""
    response = client.get("/api/v1/news_items")
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert "meta" in json, "There should be a meta object in the response"
    assert json["meta"]["limit"] == 10, "The limit should be 10"
    assert "data" in json, "There should be a data list in the response"


def test_get_news_item(client: TestClient, news_item_entity: NewsItemEntity):
    """Test the get news item api."""
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
