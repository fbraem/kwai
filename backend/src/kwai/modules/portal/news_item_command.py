"""Module that defines common command for create/update news items."""

from dataclasses import dataclass

from kwai.core.domain.use_case import TextCommand


@dataclass(kw_only=True, frozen=True, slots=True)
class NewsItemCommand:
    """Common input for the use cases "Create News Items" and "Update News Items"."""

    enabled: bool
    texts: list[TextCommand]
    application: int
    publish_datetime: str
    end_datetime: str | None
    promotion: int
    promotion_end_datetime: str | None
    remark: str
