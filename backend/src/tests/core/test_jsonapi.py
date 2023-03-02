"""Module that defines tests for JSON:API."""
import json
from dataclasses import dataclass

from pydantic import BaseModel, Field

from kwai.core import jsonapi


@jsonapi.resource(type_="members")
@dataclass
class Member:
    """A member."""

    id: int
    name: str

    @jsonapi.attribute(name="name")
    def get_name(self):
        """Return the attribute 'name'."""
        return self.name


@jsonapi.resource(type_="teams")
class Team(BaseModel):
    """A team."""

    id: int
    name: str
    members: list[Member] = Field(default_factory=list)

    @jsonapi.attribute(name="name")
    def get_name(self) -> str:
        """Return the attribute 'name'."""
        return self.name

    @jsonapi.relationship(name="members")
    def get_members(self) -> list[Member]:
        """Return the relationship 'members'."""
        return self.members


@jsonapi.resource(type_="coaches")
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

    @jsonapi.attribute()
    def name(self) -> str:
        """Return the attribute 'name'."""
        return self._name

    @jsonapi.attribute(name="year_of_birth")
    def year_of_birth(self) -> int:
        """Return the attribute 'year_of_birth'."""
        return self._year_of_birth

    @jsonapi.relationship()
    def team(self) -> Team | None:
        """Return the relationship 'team'."""
        return self._team


def test_jsonapi_common_class():
    """Test with a Python class."""
    coach = Coach(id_=1, name="Jigoro Kano", year_of_birth=1882)

    doc = jsonapi.Document(coach)
    json_api = json.loads(doc.serialize())
    assert json_api["data"]["type"] == "coaches"
    assert json_api["data"]["id"] == "1"
    assert json_api["data"]["attributes"]["name"] == "Jigoro Kano"
    assert json_api["data"]["attributes"]["year_of_birth"] == 1882


def test_jsonapi_pydantic():
    """Test with a Pydantic class."""
    team = Team(id=1, name="U15")
    doc = jsonapi.Document(team)
    json_api = json.loads(doc.serialize())
    assert json_api["data"]["type"] == "teams"
    assert json_api["data"]["id"] == "1"
    assert json_api["data"]["attributes"]["name"] == "U15"


def test_jsonapi_dataclass():
    """Test with a dataclass class."""
    member = Member(id=1, name="Kyuzo Mifune")
    doc = jsonapi.Document(member)
    json_api = json.loads(doc.serialize())
    assert json_api["data"]["type"] == "members"
    assert json_api["data"]["id"] == "1"
    assert json_api["data"]["attributes"]["name"] == "Kyuzo Mifune"


def test_jsonapi_relationship():
    """Test a relationship."""
    coach = Coach(
        id_=1, name="Jigoro Kano", year_of_birth=1882, team=Team(id=1, name="U15")
    )

    doc = jsonapi.Document(coach)
    json_api = json.loads(doc.serialize())
    assert json_api["data"]["type"] == "coaches"
    assert json_api["data"]["id"] == "1"
    assert json_api["data"]["attributes"]["name"] == "Jigoro Kano"
    assert json_api["data"]["relationships"]["team"] == {
        "data": {"type": "teams", "id": "1"}
    }
    assert "included" in json_api
