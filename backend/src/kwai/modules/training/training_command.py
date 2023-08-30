"""Module that defines common input for the use cases of Trainings."""
from dataclasses import dataclass
from typing import Any


@dataclass(kw_only=True, frozen=True, slots=True)
class Coach:
    """Input for a coach associated with a training."""

    id: int
    head: bool = False
    present: bool = False
    payed: bool = False


@dataclass(kw_only=True, frozen=True, slots=True)
class TrainingCommand:
    """Input for the create or update Training use case."""

    start_date: str
    end_date: str
    active: bool
    cancelled: bool
    location: str
    text: list[dict[str, Any]]
    remark: str
    definition: int | None
    coaches: list[Coach]
    teams: list[int]
