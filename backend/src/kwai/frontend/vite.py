"""Module for defining a class that handles files and assets created with vite."""

from abc import ABC, abstractmethod
from pathlib import Path

from kwai.frontend.manifest import Chunk, Manifest


class Vite(ABC):
    """Interface for a Vite runtime."""

    @abstractmethod
    def init(self, *entries: str):
        """Initialize the Vite runtime for the given entries."""
        raise NotImplementedError

    @abstractmethod
    def generate_scripts(self, *entries: str) -> list[str]:
        """Generate the script tags for the given entries."""
        raise NotImplementedError

    @abstractmethod
    def generate_css(self, *entries: str) -> list[str]:
        """Generate the css tags for the given entries."""
        raise NotImplementedError

    @abstractmethod
    def generate_preloads(self, *entries: str) -> list[str]:
        """Generate the preload tags for the given entries."""
        raise NotImplementedError


class DevelopmentVite(Vite):
    """Vite implementation for development."""

    def __init__(self, base_path: Path):
        self._base_path = base_path
        self._entries: list[str] = []

    def init(self, *entries: str):
        self._entries = entries

    def generate_scripts(self) -> list[str]:
        scripts = [
            f'<script type="module" src="{self._base_path}/@vite/client"></script>'
        ]
        for entry in self._entries:
            scripts.append(
                f'<script type="module" src="{self._base_path}/{entry}"></script>'
            )
        return scripts

    def generate_css(self) -> list[str]:
        return []

    def generate_preloads(self) -> list[str]:
        return []


class ProductionVite(Vite):
    """Vite implementation for production."""

    def __init__(self, manifest_filepath: Path, base_path: Path):
        self._manifest_filepath: Path = manifest_filepath
        self._base_path: Path = base_path
        self._manifest: Manifest | None = None
        self._imported_chunks: dict[str, Chunk] = {}  # chunks imported by the entries

    def init(self, *entries: str):
        """Load the manifest file."""
        self._manifest = Manifest.load_from_file(self._manifest_filepath)
        self._imported_chunks = self._find_imported_chunks(*entries)

    def generate_scripts(self) -> list[str]:
        scripts = []

        for chunk in self._imported_chunks.values():
            if chunk.entry:
                scripts.append(
                    '<script type="module" '
                    f'src="{self._base_path}/{chunk.file}"></script>'
                )

        return scripts

    def generate_css(self) -> list[str]:
        styles = []
        for chunk in self._imported_chunks.values():
            for css in chunk.css:
                styles.append(f'<link rel="stylesheet" href="{self._base_path}/{css}">')
        return styles

    def generate_preloads(self) -> list[str]:
        preloads = []

        for chunk in self._imported_chunks.values():
            if chunk.file.endswith(".js") and not chunk.entry:
                preloads.append(
                    f'<link rel="modulepreload" as="script" '
                    f'href="{self._base_path}/{chunk.file}">'
                )

        return preloads

    def _find_imported_chunks(self, *entries: str) -> dict[str, Chunk]:
        chunks = {}

        for entry in entries:
            if not self._manifest.has_chunk(entry):
                raise ValueError(f"{entry} is not a chunk in {self._manifest_filepath}")

            chunk = self._manifest.get_chunk(entry)
            if not chunk.entry:
                raise ValueError(
                    f"{entry} is not an entry point in {self._manifest_filepath}"
                )

            chunks[entry] = chunk

            imports = chunk.imports
            while imports:
                import_ = imports.pop()
                if import_ not in chunks:
                    import_chunk = self._manifest.get_chunk(import_)
                    chunks[import_] = import_chunk
                    imports.extend(import_chunk.imports)

        return chunks
