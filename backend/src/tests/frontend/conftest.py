"""Module for pytest fixtures for testing the frontend module.."""

from pathlib import Path

import pytest
from kwai.frontend.manifest import Manifest


@pytest.fixture
def manifest() -> Manifest:
    """Load a manifest file from the data folder."""
    manifest_file_path = Path(__file__).parent / "data" / "manifest.json"
    return Manifest.load_from_file(manifest_file_path)
