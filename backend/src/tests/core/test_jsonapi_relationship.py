"""Module that contains some tests for the Relationship dataclass."""
from dataclasses import dataclass, fields

from kwai.core import json_api


@dataclass(kw_only=True, frozen=True, slots=True)
class Member:
    """Test Member class."""

    first_name: str
    last_name: str


@dataclass(kw_only=True, frozen=True, slots=True)
class Team:
    """Test Team class."""

    name: str
    members: list[Member]


@dataclass(kw_only=True, frozen=True, slots=True)
class Coach:
    """Test Coach class."""

    team: Team | None
    member: Member


@dataclass(kw_only=True, frozen=True, slots=True)
class Training:
    """Test Training class."""

    coaches: list[Coach] | None


def get():
    """Pretend to be a getter for a relationship..."""


def test_relationship_optional_type():
    """Test an optional relationship."""
    relation = json_api.Relationship(
        name="team", getter=get, type=fields(Coach)[0].type
    )
    assert relation.optional, "The relationship should be optional"
    assert relation.resource_type == Team, "The resource type should be 'Team'"


def test_relationship_non_optional_type():
    """Test a non-optional relationship."""
    relation = json_api.Relationship(
        name="member", getter=get, type=fields(Coach)[1].type
    )
    assert not relation.optional, "The relationship should be not optional"
    assert relation.resource_type == Member, "The resource type should be 'Member'"


def test_relationship_list():
    """Test a list."""
    relation = json_api.Relationship(
        name="members", getter=get, type=fields(Team)[1].type
    )
    assert relation.iterable, "The relationship should be iterable"
    assert relation.resource_type == Member, "The resource type should be 'Member'"


def test_relationship_non_list():
    """Test a non-list relationship."""
    relation = json_api.Relationship(name="name", getter=get, type=fields(Team)[0].type)
    assert not relation.iterable, "The relationship should not be iterable"
    assert relation.resource_type == str, "The resource type should be 'str'"


def test_relationship_optional_list():
    """Test an optional relationship list."""
    relation = json_api.Relationship(
        name="coaches", getter=get, type=fields(Training)[0].type
    )
    assert relation.optional, "The relationship should be optional"
    assert relation.iterable, "The relationship should be iterable"
    assert relation.resource_type == Coach, "The resource type should be 'Coach'"
