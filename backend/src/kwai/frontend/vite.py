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
    def get_scripts(self, base_url: str) -> list[str]:
        """Get the scripts for the given entries."""
        raise NotImplementedError

    @abstractmethod
    def get_css(self, base_url: str) -> list[str]:
        """Get the css files for the given entries."""
        raise NotImplementedError

    @abstractmethod
    def get_preloads(self, base_url: str) -> list[str]:
        """Get the preloads for the given entries."""
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

    def __init__(self, server_url: str):
        """Initialize the development version of vite.

        Args:
            server_url: The url for the vite server

        !!! Note
            When vite is configured (see vite.config.ts) with a base then make sure that
            this base is also part of the server_url. For example: when base is
            '/apps/author' and the server is running on localhost with port 3001, then
            server_url should be: 'http://localhost:3001/apps/author'.
        """
        self._server_url = server_url
        self._entries: list[str] = []

    def init(self, *entries: str):
        self._entries = entries

    def get_scripts(self, base_url: str) -> list[str]:
        scripts = [f"{self._server_url}/@vite/client"]
        for entry in self._entries:
            scripts.append(f"{self._server_url}/{entry}")
        return scripts

    def get_css(self, base_url: str) -> list[str]:
        return []

    def get_preloads(self, base_url: str) -> list[str]:
        return []

    def get_asset_path(self, asset_path: Path) -> Path | None:
        return None


class ProductionVite(Vite):
    """Vite implementation for production."""

    def __init__(self, manifest_filepath: Path, base_path: Path):
        """Initialize the production Vite runtime.

        Args:
            manifest_filepath: Path to the manifest file.
            base_path: Path to the dist folder.

        !!! Note
            base_path is the path where the dist folder of an application is installed
            For example '/website/frontend/apps/portal' must contain a dist folder.
        """
        self._manifest_filepath: Path = manifest_filepath
        self._base_path: Path = base_path
        self._manifest: Manifest | None = None
        self._imported_chunks: dict[str, Chunk] = {}  # chunks imported by the entries

    def init(self, *entries: str):
        """Load the manifest file."""
        self._manifest = Manifest.load_from_file(self._manifest_filepath)
        self._imported_chunks = self._find_imported_chunks(*entries)

    def get_scripts(self, base_url: str) -> list[str]:
        scripts = []

        for chunk in self._imported_chunks.values():
            if chunk.entry:
                scripts.append(base_url + chunk.file)

        return scripts

    def get_css(self, base_url: str) -> list[str]:
        styles = []
        for chunk in self._imported_chunks.values():
            for css in chunk.css:
                styles.append(base_url + css)
        return styles

    def get_preloads(self, base_url: str) -> list[str]:
        preloads = []

        for chunk in self._imported_chunks.values():
            if chunk.file.endswith(".js") and not chunk.entry:
                preloads.append(base_url + chunk.file)

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
        asset_file = dist_path / path
        if asset_file.is_relative_to(dist_path) and asset_file.is_file():
            return asset_file

        return None
