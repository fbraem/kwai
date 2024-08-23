"""Module for pytest fixtures for testing the frontend module.."""

from pathlib import Path

import pytest
from kwai.frontend.manifest import Manifest


@pytest.fixture
def manifest_path() -> Path:
    """Load a manifest file from the data folder."""
    return Path(__file__).parent / "data" / "manifest.json"


@pytest.fixture
def manifest(manifest_path) -> Manifest:
    """Load a manifest file from the data folder."""
    return Manifest.load_from_file(manifest_path)
