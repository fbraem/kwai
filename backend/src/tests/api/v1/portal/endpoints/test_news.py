"""Module for testing the portal news endpoints."""
from fastapi import status
from fastapi.testclient import TestClient


def test_get_news(client: TestClient):
    """Test the get news stories api."""
    response = client.get("/api/v1/portal/news")
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert "meta" in json, "There should be a meta object in the response"
    assert json["meta"]["limit"] == 10, "The limit should be 10"
    assert "data" in json, "There should be a data list in the response"
