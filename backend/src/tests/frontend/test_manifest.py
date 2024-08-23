"""Module for testing the Manifest class."""

from pathlib import Path

import pytest
from kwai.frontend.manifest import Manifest


@pytest.fixture
def manifest() -> Manifest:
    """Load a manifest file from the data folder."""
    manifest_file_path = Path(__file__).parent / "data" / "manifest.json"
    return Manifest.load_from_file(manifest_file_path)


def test_load_manifest_from_string():
    """Test loading the manifest from a string."""
    manifest = Manifest.load_from_string(
        """
        {
          "src/index.ts": {
            "isEntry": true,
            "file": "assets/index-8a61960c.js",
            "src": "src/index.ts"
          }
        }
    """
    )
    assert len(manifest.chunks) > 0, "There should be a chunk in the manifest."
    assert manifest.has_chunk("src/index.ts") is not None, "The chunk should exist."
    assert manifest.get_chunk("src/index.ts") is not None, "The chunk should exist."


def test_chunks(manifest: Manifest):
    """Test the chunks property."""
    chunks = manifest.chunks
    assert len(chunks) > 0, "There should be chunks in the manifest."


def test_has_chunk(manifest: Manifest):
    """Test the has_chunk method."""
    assert manifest.has_chunk("src/index.ts") is True, "The chunk should exist."
    assert manifest.has_chunk("images/hero.jpg") is True, "The chunk should exist."


def test_chunk(manifest: Manifest):
    """Test the get_chunk method."""
    chunk = manifest.get_chunk("src/index.ts")
    assert chunk is not None, "The chunk should exist."
    assert chunk.src == "src/index.ts", "The src should be 'src/index.ts'"
    assert chunk.file == "assets/index-533fa9ea.js"
    assert len(chunk.imports) > 0
    assert chunk.entry is True
    assert len(chunk.assets) > 0
    assert len(chunk.css) > 0
    assert len(chunk.dynamic_imports) > 0
    assert chunk.dynamic_entry is False
