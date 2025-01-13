"""Module that defines a class for handling the manifest file of Vite."""

import json

from dataclasses import dataclass, field
from pathlib import Path
from typing import Self


@dataclass(frozen=True, kw_only=True, slots=True)
class Chunk:
    """An entry of a manifest file."""

    src: str | None = None
    name: str | None = None
    entry: bool = False
    dynamic_entry: bool = False
    file: str
    css: list[str] = field(default_factory=list)
    assets: list[str] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)
    dynamic_imports: list[str] = field(default_factory=list)


class Manifest:
    """Class for handling a manifest file of Vite."""

    def __init__(self, entries: dict[str, Chunk]) -> None:
        """Initialize the Manifest class."""
        self._entries = entries

    @property
    def chunks(self):
        """Return the entries."""
        return self._entries.copy()

    def has_chunk(self, entry_name: str):
        """Check if the entry exists in the manifest file."""
        return entry_name in self._entries

    def get_chunk(self, entry_name: str) -> Chunk:
        """Return the entry with the given name."""
        return self._entries[entry_name]

    @classmethod
    def load_from_file(cls, file_path: Path) -> Self:
        """Load the manifest from a file."""
        with open(file_path, "r") as manifest_file:
            return cls.load_from_string(manifest_file.read())

    @classmethod
    def load_from_string(cls, content: str) -> Self:
        """Load the manifest from a string."""
        entries: dict[str, Chunk] = {}
        json_data = json.loads(content)
        for k, v in json_data.items():
            if not isinstance(v, dict):
                continue
            entry = Chunk(
                src=v.get("src", None),
                name=v.get("name", None),
                entry=v.get("isEntry", False),
                dynamic_entry=v.get("isDynamicEntry", False),
                file=v.get("file"),
                css=v.get("css", []),
                assets=v.get("assets", []),
                imports=v.get("imports", []),
                dynamic_imports=v.get("dynamicImports", []),
            )
            entries[k] = entry

        return cls(entries=entries)
