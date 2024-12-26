"""Module for testing the development vite class."""

import pytest

from kwai.frontend.vite import DevelopmentVite, Vite


@pytest.fixture
def vite() -> Vite:
    """A fixture for vite development."""
    vite = DevelopmentVite("http://localhost:5173")
    vite.init("src/index.ts")
    return vite


def test_development_vite_scripts(vite: Vite):
    """Test the development version of the Vite class for script tags."""
    scripts = vite.get_scripts("")
    assert len(scripts) == 2, "There should be 2 script tags"
    assert scripts[0] == "http://localhost:5173/@vite/client"
    assert scripts[1] == "http://localhost:5173/src/index.ts"


def test_development_vite_css(vite: Vite):
    """Test the development version of the Vite class for css tags."""
    assert len(vite.get_css("")) == 0, "There should be no css in development"


def test_development_vite_preload(vite: Vite):
    """Test the development version of the Vite class for preload tags."""
    assert len(vite.get_preloads("")) == 0, "There should be no preload in development"
