"""Module that defines tests for JSON:API."""
from dataclasses import dataclass

from pydantic import BaseModel, Field

from kwai.core import json_api
from kwai.core.json_api import JsonApiRelationship, JsonApiResourceIdentifier


@json_api.resource(type_="members")
@dataclass
class Member:
    """A member."""

    id: int
    name: str

    @json_api.attribute(name="name")
    def get_name(self):
        """Return the attribute 'name'."""
        return self.name


@json_api.resource(type_="teams")
class Team(BaseModel):
    """A team."""

    id: int
    name: str
    members: list[Member] = Field(default_factory=list)

    @json_api.attribute(name="name")
    def get_name(self) -> str:
        """Return the attribute 'name'."""
        return self.name

    @json_api.relationship(name="members")
    def get_members(self) -> list[Member]:
        """Return the relationship 'members'."""
        return self.members


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

    def id(self):
        """Return the id."""
        return self._id

    @json_api.attribute()
    def name(self) -> str:
        """Return the attribute 'name'."""
        return self._name

    @json_api.attribute(name="year_of_birth")
    def year_of_birth(self) -> int:
        """Return the attribute 'year_of_birth'."""
        return self._year_of_birth

    @json_api.relationship()
    def team(self) -> Team | None:
        """Return the relationship 'team'."""
        return self._team


def test_jsonapi_common_class():
    """Test with a Python class."""
    coach = Coach(id_=1, name="Jigoro Kano", year_of_birth=1882)

    doc = json_api.Document(coach)
    json_api_document = doc.serialize()
    assert json_api_document.data.type == "coaches"
    assert json_api_document.data.id == "1"
    assert json_api_document.data.attributes["name"] == "Jigoro Kano"
    assert json_api_document.data.attributes["year_of_birth"] == 1882


def test_jsonapi_pydantic():
    """Test with a Pydantic class."""
    team = Team(id=1, name="U15")
    doc = json_api.Document(team)
    json_api_document = doc.serialize()
    assert json_api_document.data.type == "teams"
    assert json_api_document.data.id == "1"
    assert json_api_document.data.attributes["name"] == "U15"


def test_jsonapi_dataclass():
    """Test with a dataclass class."""
    member = Member(id=1, name="Kyuzo Mifune")
    doc = json_api.Document(member)
    json_api_document = doc.serialize()
    assert json_api_document.data.type == "members"
    assert json_api_document.data.id == "1"
    assert json_api_document.data.attributes["name"] == "Kyuzo Mifune"


def test_jsonapi_relationship():
    """Test a relationship."""
    coach = Coach(
        id_=1, name="Jigoro Kano", year_of_birth=1882, team=Team(id=1, name="U15")
    )

    doc = json_api.Document(coach)
    json_api_document = doc.serialize()
    assert json_api_document.data.type == "coaches"
    assert json_api_document.data.id == "1"
    assert json_api_document.data.attributes["name"] == "Jigoro Kano"
    assert json_api_document.data.relationships["team"] == JsonApiRelationship(
        data=JsonApiResourceIdentifier(type="teams", id="1")
    )
    assert len(json_api_document.included) == 1, "There should be an included resource"
    # pylint: disable=unsubscriptable-object
    assert json_api_document.included[0].type == "teams"
    assert json_api_document.included[0].id == "1"
    assert json_api_document.included[0].attributes["name"] == "U15"
