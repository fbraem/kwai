"""Module that defines a value object for text content."""
from dataclasses import dataclass, field

from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.traceable_time import TraceableTime


@dataclass(frozen=True, kw_only=True, slots=True)
class Content:
    """Value object for the content of a news story.

    Attributes:
        locale: The locale of the content.
        format: The format of the content.
        title: The title of the content.
        content: The long text of the content.
        summary: The summary of the content.
        author: The author of the content.
        traceable_time: The creation and modification timestamp of the content.
    """

    locale: str
    format: str
    title: str
    content: str
    summary: str
    author: Owner
    traceable_time: TraceableTime = field(default_factory=TraceableTime)
