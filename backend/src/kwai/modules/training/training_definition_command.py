"""Module that defines the common input for the use cases Training Definitions."""
from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True, slots=True)
class TrainingDefinitionCommand:
    """Input for the create or update Training Definition use case."""

    name: str
    description: str
    weekday: int
    start_time: str
    end_time: str
    active: bool
    location: str
    remark: str | None
    team_id: int | None
