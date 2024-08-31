"""Module that defines the routes for the portal frontend application."""

from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from kwai.api.dependencies import create_templates
from kwai.core.settings import FrontendApplicationSettings, get_settings
from kwai.frontend.dependencies import FrontendApplicationDependency, ViteDependency
from kwai.frontend.vite import Vite

APP_NAME = "portal"

router = APIRouter(prefix=f"/{APP_NAME}")

_portal_dependency = FrontendApplicationDependency(APP_NAME)
_portal_vite_dependency = ViteDependency(APP_NAME)

settings = get_settings()
if not settings.frontend.test:
    root_path = Path(settings.frontend.path) / "apps" / APP_NAME / "dist"
    # Public files
    router.mount("/public", StaticFiles(directory=root_path))
    # Assets
    router.mount("/assets", StaticFiles(directory=root_path / "assets"))


@router.get("/{router:path}")
async def get_app(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(create_templates)],
    app_settings: Annotated[FrontendApplicationSettings, Depends(_portal_dependency)],
    vite: Annotated[Vite, Depends(_portal_vite_dependency)],
):
    print("Portal???")
    return templates.TemplateResponse(
        "index.jinja2",
        {
            "request": request,
            "vite": vite,
        },
    )
