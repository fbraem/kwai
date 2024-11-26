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

    @abstractmethod
    def get_asset_path(self, asset_path: Path) -> Path | None:
        """Return the path for an asset.

        None is returned when the file should not be processed. This is the case
        in the development environment, because Vite will serve the assets.

        None should also be returned when the file does not exist in the dist folder.
        This way, the url path will be handled by Vue Router.

        When the path starts with public, the path without 'public' is used to search
        the file in the dist folder.
        """


class DevelopmentVite(Vite):
    """Vite implementation for development."""

    def __init__(self, base_path: str):
        """Initialize the development version of vite.

        Args:
            base_path: The base path for the development version of vite.

        !!! Note
            When vite is configured with a base then make sure that this
            base is also part of the base_path argument. For example: when base is
            '/apps/author' and the server is running on localhost with port 3001, then
            base_path should be: 'http://localhost:3001/apps/author'.
        """
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

    def get_asset_path(self, path: Path) -> Path | None:
        return None


class ProductionVite(Vite):
    """Vite implementation for production."""

    def __init__(self, manifest_filepath: Path, base_path: Path):
        """Initialize the production Vite runtime.

        Args:
            manifest_filepath: Path to the manifest file.
            base_path: Path to the dist folder.
        """
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
                scripts.append('<script type="module" ' f'src="{chunk.file}"></script>')

        return scripts

    def generate_css(self) -> list[str]:
        styles = []
        for chunk in self._imported_chunks.values():
            for css in chunk.css:
                styles.append(f'<link rel="stylesheet" href="{css}">')
        return styles

    def generate_preloads(self) -> list[str]:
        preloads = []

        for chunk in self._imported_chunks.values():
            if chunk.file.endswith(".js") and not chunk.entry:
                preloads.append(
                    f'<link rel="modulepreload" as="script" ' f'href="{chunk.file}">'
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

    def get_asset_path(self, path: Path) -> Path | None:
        dist_path = self._base_path / "dist"
        if len(path.parents) > 0 and str(path.parents[0]) == "public":
            path = Path(*path.parts[1:])
        asset_file = dist_path / path
        if asset_file.is_relative_to(dist_path) and asset_file.is_file():
            return asset_file

        return None
