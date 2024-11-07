"""Module that defines the routes for the authentication frontend application."""

from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from kwai.api.dependencies import create_templates
from kwai.frontend.dependencies import ViteDependency
from kwai.frontend.etag_file_response import EtagFileResponse
from kwai.frontend.vite import Vite

APP_NAME = "auth"

router = APIRouter(prefix=f"/{APP_NAME}")

_auth_vite_dependency = ViteDependency(APP_NAME)


@router.get("/{path:path}")
async def get_app(
    path: Path,
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(create_templates)],
    vite: Annotated[Vite, Depends(_auth_vite_dependency)],
):
    asset_file_path = vite.get_asset_path(path)
    if asset_file_path is not None:
        return EtagFileResponse(asset_file_path)

    return templates.TemplateResponse(
        "index.jinja2",
        {
            "request": request,
            "vite": vite,
        },
    )
