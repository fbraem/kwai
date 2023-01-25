"""Module that defines a dependency for a template engine."""
from fastapi import Depends

from kwai.core.settings import get_settings
from kwai.core.template.template_engine import TemplateEngine
from kwai.core.template.jinja2_engine import Jinja2Engine


def get_template_engine(settings=Depends(get_settings)) -> TemplateEngine:
    """Get the template engine."""
    return Jinja2Engine(settings.template_path, website=settings.website.dict())
