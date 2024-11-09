"""Module for testing the development vite class."""

from pathlib import Path

import pytest

from kwai.frontend.vite import DevelopmentVite, Vite


@pytest.fixture
def vite() -> Vite:
    """A fixture for vite development."""
    vite = DevelopmentVite(Path("http://localhost:5173"))
    vite.init("src/index.ts")
    return vite


def test_development_vite_scripts(vite: Vite):
    """Test the development version of the Vite class for script tags."""
    scripts = vite.generate_scripts()
    assert len(scripts) == 2, "There should be 2 script tags"
    assert (
        scripts[0]
        == '<script type="module" src="http:/localhost:5173/@vite/client"></script>'
    )
    assert (
        scripts[1]
        == '<script type="module" src="http:/localhost:5173/src/index.ts"></script>'
    )


def test_development_vite_css(vite: Vite):
    """Test the development version of the Vite class for css tags."""
    assert len(vite.generate_css()) == 0, "There should be no css in development"


def test_development_vite_preload(vite: Vite):
    """Test the development version of the Vite class for preload tags."""
    assert (
        len(vite.generate_preloads()) == 0
    ), "There should be no preload in development"
