"""Module for testing the production vite class."""

from pathlib import Path

import pytest

from kwai.frontend.vite import ProductionVite, Vite


@pytest.fixture
def vite(manifest_path: Path, tmp_path: Path) -> Vite:
    """A fixture for vite production."""
    vite = ProductionVite(manifest_path, tmp_path)
    vite.init("src/index.ts")
    return vite


def test_production_vite_scripts(vite: Vite):
    """Test the production version of the Vite class for script tags."""
    scripts = vite.get_scripts("http://localhost:8000/apps/portal/")
    assert len(scripts) == 1, "There should be one script tag"
    assert scripts[0] == "http://localhost:8000/apps/portal/assets/index-533fa9ea.js"


def test_production_vite_css(vite: Vite):
    """Test the production of the Vite class for css tags."""
    css = vite.get_css("")
    assert len(css) == 1, "There should be a css link"
    assert css[0] == "assets/index-ace45c09.css"


def test_production_vite_preload(vite: Vite):
    """Test the production version of the Vite class for preload tags."""
    preload = vite.get_preloads("")
    assert len(preload) == 1, "There should be a preload"
    assert preload[0] == "assets/vendor-97e41b2b.js"


def test_production_vite_get_asset_path(vite: Vite, tmp_path: Path):
    """Test getting the path of an asset."""
    dist_path = tmp_path / "dist"
    dist_path.mkdir(exist_ok=True)
    with open(dist_path / "test_file.txt", "w") as f:
        f.write("This is a test file.")

    asset_file = vite.get_asset_path(Path("test_file.txt"))
    assert asset_file is not None


def test_production_vite_get_public_path(vite: Vite, tmp_path: Path):
    """Test getting the path of a public file."""
    dist_path = tmp_path / "dist"
    dist_path.mkdir(exist_ok=True)
    with open(dist_path / "test_file.txt", "w") as f:
        f.write("This is a test file.")

    asset_file = vite.get_asset_path(Path("test_file.txt"))
    assert asset_file is not None


def test_production_vite_get_asset_path_with_relative(vite: Vite, tmp_path: Path):
    """Test if a relative path fails."""
    dist_path = tmp_path / "dist"
    dist_path.mkdir(exist_ok=True)
    with open(dist_path / "test_file.txt", "w") as f:
        f.write("This is a test file.")

    asset_file = vite.get_asset_path(Path("../../test_file.txt"))
    assert asset_file is None
