"""Module for defining the Author entity."""

from dataclasses import dataclass
from typing import ClassVar, Type

from kwai.core.domain.entity import DataclassEntity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.unique_id import UniqueId


class AuthorIdentifier(IntIdentifier):
    """Identifier for an author entity."""


@dataclass(kw_only=True, eq=False, slots=True, frozen=True)
class AuthorEntity(DataclassEntity):
    """An author entity."""

    ID: ClassVar[Type] = AuthorIdentifier

    uuid: UniqueId
    name: str = ""
    active: bool = True
    remark: str = ""
