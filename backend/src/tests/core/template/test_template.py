"""Module for testing Template class."""

from kwai.core.template.jinja2_engine import Jinja2Engine
from kwai.frontend.vite import DevelopmentVite


def test_render():
    """Test render."""
    engine = Jinja2Engine(website={"name": "Kwai Test"})
    template = engine.create("index.jinja2")
    result = template.render(
        vite=DevelopmentVite("", ""), application={"name": "test", "url": "test"}
    )

    assert result is not None, "The template didn't render the correct output"
