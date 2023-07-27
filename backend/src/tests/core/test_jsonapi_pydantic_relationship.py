"""Module that contains some tests for the Relationship dataclass."""
from pydantic import BaseModel

from kwai.core import json_api


class Member(BaseModel):
    """Test Member class."""

    first_name: str
    last_name: str


class Team(BaseModel):
    """Test Team class."""

    name: str
    members: list[Member]


class Coach(BaseModel):
    """Test Coach class."""

    team: Team | None
    member: Member


class Training(BaseModel):
    """Test Training class."""

    coaches: list[Coach] | None


def get():
    """Pretend to be a getter for a relationship..."""


def test_relationship_optional_type():
    """Test an optional relationship."""
    relation = json_api.Relationship(
        name="team", getter=get, type=Coach.__fields__["team"].annotation
    )
    assert relation.optional, "The relationship should be optional"
    assert relation.resource_type == Team, "The resource type should be 'Team'"


def test_relationship_non_optional_type():
    """Test a non-optional relationship."""
    relation = json_api.Relationship(
        name="member", getter=get, type=Coach.__fields__["member"].annotation
    )
    assert not relation.optional, "The relationship should be not optional"
    assert relation.resource_type == Member, "The resource type should be 'Member'"


def test_relationship_list():
    """Test a relationship list."""
    relation = json_api.Relationship(
        name="members", getter=get, type=Team.__fields__["members"].annotation
    )
    assert relation.iterable, "The relationship should be iterable"
    assert relation.resource_type == Member, "The resource type should be 'Member'"


def test_relationship_non_list():
    """Test a non list relationship."""
    relation = json_api.Relationship(
        name="name", getter=get, type=Team.__fields__["name"].annotation
    )
    assert not relation.iterable, "The relationship should not be iterable"
    assert relation.resource_type == str, "The resource type should be 'str'"


def test_relationship_optional_list():
    """Test an optional relationship."""
    relation = json_api.Relationship(
        name="coaches", getter=get, type=Training.__fields__["coaches"].annotation
    )
    assert relation.optional, "The relationship should be optional"
    assert relation.iterable, "The relationship should be iterable"
    assert relation.resource_type == Coach, "The resource type should be 'Coach'"
