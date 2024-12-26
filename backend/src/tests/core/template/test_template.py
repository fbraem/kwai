"""Module for testing Template class."""

from kwai.core.template.jinja2_engine import Jinja2Engine
from kwai.frontend.vite import DevelopmentVite


def test_render():
    """Test render."""
    engine = Jinja2Engine(website={"name": "Kwai Test"})
    template = engine.create("index")
    result = template.render(
        vite=DevelopmentVite("https://localhost:3000/apps/portal"),
        application={"name": "test", "url": "test"},
    )

    assert result is not None, "The template didn't render the correct output"
