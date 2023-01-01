import os

from kwai.core.template.jinja2_engine import Jinja2Engine


def test_render():
    template_path = os.path.split(__file__)[0]
    engine = Jinja2Engine(template_path, website={"name": "Kwai Test"})
    template = engine.create("template")
    result = template.render()

    assert result == "Kwai Test", "The template didn't render the correct output"
