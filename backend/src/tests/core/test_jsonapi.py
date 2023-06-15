"""Module that defines tests for JSON:API."""
from dataclasses import dataclass

from pydantic import BaseModel, Field

from kwai.core import json_api


@json_api.resource(type_="members")
@dataclass
class Member:
    """A member."""

    id: int
    name: str


@json_api.resource(type_="teams")
class Team(BaseModel):
    """A team."""

    id: int
    name: str
    members: list[Member] = Field(default_factory=list)


@json_api.resource(type_="coaches")
class Coach:
    """A coach."""

    def __init__(
        self, *, id_: int, name: str, year_of_birth: int, team: Team | None = None
    ):
        self._id = id_
        self._name = name
        self._year_of_birth = year_of_birth
        self._team = team

    @json_api.id
    def id(self):
        """Return the id."""
        return self._id

    @json_api.attribute
    def name(self) -> str:
        """Return the attribute 'name'."""
        return self._name

    @json_api.attribute(name="year_of_birth")
    def year_of_birth(self) -> int:
        """Return the attribute 'year_of_birth'."""
        return self._year_of_birth

    @json_api.relationship
    def team(self) -> Team | None:
        """Return the relationship 'team'."""
        return self._team


def test_jsonapi_resource():
    """Test the resource class."""
    resource = json_api.Resource(Coach).build()
    assert (
        resource.get_attribute("name") is not None
    ), "There should be a name attribute."
    assert (
        resource.get_attribute("year_of_birth") is not None
    ), "There should be a year of birth attribute."
    assert resource.get_type() == "coaches", "The resource type should be 'coaches'."
    assert resource.has_id(), "There should be a way to get the id."
    assert (
        resource.get_relationship("team") is not None
    ), "There should be a 'team' relationship."


def test_jsonapi_dataclass_resource():
    """Test the resource class with a dataclass."""
    resource = json_api.Resource(Member).build()
    assert (
        resource.get_attribute("name") is not None,
        "There should be a name attribute",
    )
    assert resource.has_id(), "There should be a way to get the id."
    assert resource.get_type() == "members", "The resource type should be 'members'."


def test_jsonapi_basemodel_resource():
    """Test the resource class with a pydantic BaseModel."""
    resource = json_api.Resource(Team).build()
    assert (
        resource.get_attribute("name") is not None,
        "There should be a name attribute",
    )
    assert resource.has_id(), "There should be a way to get the id."
    assert resource.get_type() == "teams", "The resource type should be 'teams'."
    assert resource.get_relationship(
        "members"
    ), "There should be a relationship 'members'."


def test_jsonapi_resource_decorator():
    """Test if the class contains a resource and a type."""
    resource = getattr(Coach, "__json_api_resource__", None)
    assert (
        resource is not None
    ), "There should be a __json_api_resource__ attribute defined on the class."

    assert resource.get_type() == "coaches", "The type should be 'coaches'."


def test_resource_identifier_model():
    """Test if the resource identifier model is created correctly."""
    resource = json_api.Resource(Coach).build()
    resource_identifier = resource.get_resource_identifier_model()
    assert (
        resource_identifier is not None
    ), "There should be a resource identifier model"
    resource_identifier_instance = resource_identifier()
    assert (
        resource_identifier_instance.type == "coaches"
    ), "The type should be 'coaches'"


def test_resource_model():
    """Test if the resource identifier model is created correctly."""
    resource = json_api.Resource(Coach).build()
    resource_model = resource.get_resource_model()
    assert resource_model is not None, "There should be a resource model"
    resource_instance = resource_model(
        id="1",
        attributes={"name": "Jigoro Kano", "year_of_birth": 1882},
        relationships={"team": {"data": None}},
    )
    assert (
        resource_instance.attributes.name == "Jigoro Kano"
    ), "The name should be 'Jigoro Kano'"
    assert (
        resource_instance.attributes.year_of_birth == 1882
    ), "The year of birth should be 1882"


def test_document_model():
    resource = json_api.Resource(Coach).build()
    document_model = resource.get_document_model()
    assert document_model is not None, "There should be a document model"
    print(document_model.schema_json(indent=2))


def test_jsonapi_common_class():
    """Test with a Python class."""
    coach = Coach(id_=1, name="Jigoro Kano", year_of_birth=1882)

    json_api_document = coach.serialize()
    print(json_api_document)
    assert json_api_document.data.type == "coaches"
    assert json_api_document.data.id == "1"
    assert json_api_document.data.attributes.name == "Jigoro Kano"
    assert json_api_document.data.attributes.year_of_birth == 1882


def test_jsonapi_pydantic():
    """Test with a Pydantic class."""
    team = Team(id=1, name="U15")
    json_api_document = team.serialize()
    assert json_api_document.data.type == "teams"
    assert json_api_document.data.id == "1"
    assert json_api_document.data.attributes.name == "U15"


def test_jsonapi_dataclass():
    """Test with a dataclass class."""
    member = Member(id=1, name="Kyuzo Mifune")
    json_api_document = member.serialize()
    print(json_api_document)
    assert json_api_document.data.type == "members"
    assert json_api_document.data.id == "1"
    assert json_api_document.data.attributes.name == "Kyuzo Mifune"


def test_jsonapi_relationship():
    """Test a relationship."""
    team = Team(id=1, name="U15")
    coach = Coach(id_=1, name="Jigoro Kano", year_of_birth=1882, team=team)
    json_api_document = coach.serialize()
    print(json_api_document.json())
    assert json_api_document.data.type == "coaches"
    assert json_api_document.data.id == "1"
    assert json_api_document.data.attributes.name == "Jigoro Kano"
    assert json_api_document.data.relationships.team is not None
    # assert len(json_api_document.included) > 0, "There should be an included resource"
    # pylint: disable=unsubscriptable-object
    # assert json_api_document.included[0].type == "teams"
    # assert json_api_document.included[0].id == "1"
    # assert json_api_document.included[0].attributes.name == "U15"


def test_jsonapi_auto_relationship():
    """Test a relationship."""
    team = Team(id=1, name="U15")
    team.members.append(Member(id=1, name="Kyuzo Mifune"))

    json_api_document = team.serialize()
    assert json_api_document.data.type == "teams"
    assert json_api_document.data.id == "1"
    assert json_api_document.data.attributes.name == "U15"
    assert isinstance(json_api_document.data.relationships.members.data, list)
    # assert len(json_api_document.included) > 0, "There should be an included resource"
    # pylint: disable=unsubscriptable-object
    # assert json_api_document.included[0].type == "members"
    # assert json_api_document.included[0].id == "1"
    # assert json_api_document.included[0].attributes["name"] == "Kyuzo Mifune"
