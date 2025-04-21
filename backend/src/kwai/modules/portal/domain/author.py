"""Module for defining the Author entity."""

from dataclasses import dataclass
from typing import ClassVar, Type

from kwai.core.domain.entity import DataclassEntity
from kwai.modules.identity.users.user import UserIdentifier


@dataclass(kw_only=True, eq=False, slots=True, frozen=True)
class AuthorEntity(DataclassEntity):
    """An author entity."""

    ID: ClassVar[Type] = UserIdentifier

    name: str = ""
    active: bool = True
    remark: str = ""
