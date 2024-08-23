"""Module for testing the production vite class."""

from pathlib import Path

import pytest
from kwai.frontend.vite import ProductionVite, Vite


@pytest.fixture
def vite(manifest_path: Path) -> Vite:
    """A fixture for vite production."""
    vite = ProductionVite(manifest_path, Path("/home/kwai/website"))
    vite.init("src/index.ts")
    return vite


def test_production_vite_scripts(vite: Vite):
    """Test the production version of the Vite class for script tags."""
    scripts = vite.generate_scripts()
    assert len(scripts) == 1, "There should be one script tag"
    assert (
        scripts[0] == '<script type="module" '
        'src="/home/kwai/website/assets/index-533fa9ea.js"></script>'
    )


def test_production_vite_css(vite: Vite):
    """Test the production of the Vite class for css tags."""
    css = vite.generate_css()
    assert len(css) == 1, "There should be a css link"
    assert (
        css[0]
        == '<link rel="stylesheet" href="/home/kwai/website/assets/index-ace45c09.css">'
    )


def test_production_vite_preload(vite: Vite):
    """Test the production version of the Vite class for preload tags."""
    preload = vite.generate_preloads()
    assert len(preload) == 1, "There should be a preload"
    assert (
        preload[0]
        == '<link rel="modulepreload" as="script" href="/home/kwai/website/assets/vendor-97e41b2b.js">'
    )
