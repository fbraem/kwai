"""Module for testing the JSON:API models."""

from types import NoneType
from typing import Literal

import pytest
from pydantic import BaseModel
from rich import json

from kwai.core.json_api import Document, Error, ResourceData, ResourceIdentifier


class JudokaResourceIdentifier(ResourceIdentifier):
    """A JSON:API resource identifier for a judoka."""

    type: Literal["judokas"] = "judokas"


def test_judoka_resource_identifier():
    """Test a JSON:API resource identifier."""
    id = JudokaResourceIdentifier(id="1")
    assert id.type == "judokas", "Type should be 'judokas'"


class JudokaAttributes(BaseModel):
    """Attributes for a JSON:API resource of a judoka."""

    name: str
    birth_date: str


class JudokaResource(
    JudokaResourceIdentifier, ResourceData[JudokaAttributes, NoneType]
):
    """A JSON:API resource for a judokas."""


@pytest.fixture
def judoka_resource() -> JudokaResource:
    """A fixture for a JSON:API resource of a judoka."""
    return JudokaResource(
        id="1", attributes=JudokaAttributes(name="Jigoro Kano", birth_date="18601210")
    )


def test_resource_attributes(judoka_resource: JudokaResource):
    """Test the attributes of a JSON:API resource."""
    assert judoka_resource.id == "1", "The id of the judoka should be '1'."
    assert (
        judoka_resource.attributes.name == "Jigoro Kano"
    ), "The judoka should have a name."


class JudokaDocument(Document[JudokaResource, NoneType]):
    """A JSON:API document for a judoka."""


def test_dump_json(judoka_resource: JudokaResource):
    """Test if the serialized json structure is correct."""
    document = JudokaDocument(data=judoka_resource)
    json_doc = json.loads(document.model_dump_json())
    assert "data" in json_doc, "There should be a 'data' key"
    assert "id" in json_doc["data"], "There should be an 'id' in the document."
    assert json_doc["data"]["id"] == "1", "The id should be '1'."
    assert "type" in json_doc["data"], "There should be a 'type' in the document."
    assert json_doc["data"]["type"] == "judokas", "The type should be 'judoka'."
    assert (
        "attributes" in json_doc["data"]
    ), "There should be a 'attributes' in the document."
    assert (
        "name" in json_doc["data"]["attributes"]
    ), "There should be a 'name' in the attributes."
    assert (
        json_doc["data"]["attributes"]["name"] == "Jigoro Kano"
    ), "The judoka should have a name."


def test_error():
    """Test the error of a JSON:API document."""
    json_doc = JudokaDocument(
        data=[],
        errors=[
            Error(
                title="No judoka selected",
                detail="There is no judoka selected for this tournament",
            )
        ],
    )
    json_doc = json.loads(json_doc.model_dump_json())
    assert "errors" in json_doc, "There should be a 'errors' in the document."
    assert json_doc["errors"][0]["title"] == "No judoka selected"