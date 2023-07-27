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


def test_jsonapi_resource_decorator():
    """Test if the class contains a resource and a type."""
    resource = getattr(Coach, "__json_api_resource__", None)
    assert (
        resource is not None
    ), "There should be a __json_api_resource__ attribute defined on the class."

    assert resource.get_type() == "coaches", "The type should be 'coaches'."


def test_jsonapi_resource():
    """Test the resource class."""
    json_api.Resource(Coach).build()
    assert (
        Coach.__json_api_resource__.get_attribute("name") is not None
    ), "There should be a name attribute."
    assert (
        Coach.__json_api_resource__.get_attribute("year_of_birth") is not None
    ), "There should be a year of birth attribute."
    assert (
        Coach.__json_api_resource__.get_type() == "coaches"
    ), "The resource type should be 'coaches'."
    assert Coach.__json_api_resource__.has_id(), "There should be a way to get the id."
    assert (
        Coach.__json_api_resource__.get_relationship("team") is not None
    ), "There should be a 'team' relationship."


def test_jsonapi_dataclass_resource():
    """Test the resource class with a dataclass."""
    assert (
        Member.__json_api_resource__.get_attribute("name") is not None
    ), "There should be a name attribute"

    assert Member.__json_api_resource__.has_id(), "There should be a way to get the id."
    assert (
        Member.__json_api_resource__.get_type() == "members"
    ), "The resource type should be 'members'."


def test_jsonapi_basemodel_resource():
    """Test the resource class with a pydantic BaseModel."""
    assert (
        Team.__json_api_resource__.get_attribute("name") is not None
    ), "There should be a name attribute"
    assert Team.__json_api_resource__.has_id(), "There should be a way to get the id."
    assert (
        Team.__json_api_resource__.get_type() == "teams"
    ), "The resource type should be 'teams'."
    assert Team.__json_api_resource__.get_relationship(
        "members"
    ), "There should be a relationship 'members'."


def test_resource_identifier_model():
    """Test if the resource identifier model is created correctly."""
    resource_identifier = Coach.__json_api_resource__.get_resource_identifier_model()
    assert (
        resource_identifier is not None
    ), "There should be a resource identifier model"
    resource_identifier_instance = resource_identifier()
    assert (
        resource_identifier_instance.type == "coaches"
    ), "The type should be 'coaches'"


def test_resource_model():
    """Test if the resource identifier model is created correctly."""
    resource_model = Coach.__json_api_resource__.get_resource_model()
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
    """Test the creation of a document model."""
    document_model = Coach.get_document_model()

    assert document_model is not None, "There should be a document model"


def test_jsonapi_common_class():
    """Test with a Python class."""
    coach = Coach(id_=1, name="Jigoro Kano", year_of_birth=1882)

    json_api_document = coach.serialize()

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

    assert json_api_document.data.type == "members"
    assert json_api_document.data.id == "1"
    assert json_api_document.data.attributes.name == "Kyuzo Mifune"


def test_jsonapi_relationship():
    """Test a relationship."""
    team = Team(id=1, name="U15")
    coach = Coach(id_=1, name="Jigoro Kano", year_of_birth=1882, team=team)

    json_api_document = coach.serialize()

    assert json_api_document.data.type == "coaches"
    assert json_api_document.data.id == "1"
    assert json_api_document.data.attributes.name == "Jigoro Kano"
    assert json_api_document.data.relationships.team is not None
    assert len(json_api_document.included) > 0, "There should be an included resource"
    assert json_api_document.included[0].type == "teams"
    assert json_api_document.included[0].id == "1"
    assert json_api_document.included[0].attributes.name == "U15"


def test_jsonapi_auto_relationship():
    """Test a relationship."""
    team = Team(id=1, name="U15")
    team.members.append(Member(id=1, name="Kyuzo Mifune"))

    json_api_document = team.serialize()

    assert json_api_document.data.type == "teams"
    assert json_api_document.data.id == "1"
    assert json_api_document.data.attributes.name == "U15"
    assert isinstance(json_api_document.data.relationships.members.data, list)
    assert len(json_api_document.included) > 0, "There should be an included resource"
    assert json_api_document.included[0].type == "members"
    assert json_api_document.included[0].id == "1"
    assert json_api_document.included[0].attributes.name == "Kyuzo Mifune"


def test_multiple_relationships():
    """Test a resource with multiple relations."""
    team = Team(id=1, name="U15")
    team.members.append(Member(id=1, name="Kyuzo Mifune"))
    team.members.append(Member(id=2, name="Jigoro Kano"))

    json_api_document = team.serialize()
    assert (
        len(json_api_document.included) == 2
    ), "There should be an 2 included resources"

    def search_member(id: str):
        for resource in json_api_document.included:
            if resource.type == "members" and resource.id == id:
                return resource

    member = search_member("1")
    assert member is not None, "There should be a member with id '1'"
    assert (
        member.attributes.name == "Kyuzo Mifune"
    ), "The name of member '1' should be 'Kyuzo Mifune'"
    member = search_member("2")
    assert member is not None, "There should be a member with id '2'"
    assert (
        member.attributes.name == "Jigoro Kano"
    ), "The name of member '2' should be 'Jigoro Kano'"


def test_multiple_resource_list():
    """Test serializing a list of resources."""
    teams = [
        Team(id=1, name="U15", members=[Member(id=1, name="Jigoro Kano")]),
        Team(id=2, name="U18", members=[Member(id=2, name="Kyuzo Mifune")]),
    ]
    json_api_document = Team.serialize_list(teams)
    assert len(json_api_document.data) == 2, "There should be 2 team resources"
    assert len(json_api_document.included) == 2, "There should be 2 related resources"
