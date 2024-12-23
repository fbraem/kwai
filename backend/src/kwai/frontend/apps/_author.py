"""Module that defines the routes for the author frontend application."""

from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from kwai.api.dependencies import create_templates
from kwai.frontend.dependencies import ViteDependency
from kwai.frontend.etag_file_response import EtagFileResponse
from kwai.frontend.vite import Vite

APP_NAME = "author"

router = APIRouter(prefix=f"/{APP_NAME}")

_auth_vite_dependency = ViteDependency(APP_NAME)


@router.get("/{path:path}", name=APP_NAME)
async def get_app(
    path: Path,
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(create_templates)],
    vite: Annotated[Vite, Depends(_auth_vite_dependency)],
):
    asset_file_path = vite.get_asset_path(path)
    if asset_file_path is not None:
        return EtagFileResponse(asset_file_path)

    url = request.url_for(APP_NAME, path="")
    if "x-forwarded-proto" in request.headers:
        url = url.replace(scheme=request.headers["x-forwarded-proto"])

    return templates.TemplateResponse(
        "index.jinja2",
        {
            "application": {
                "name": APP_NAME,
                "url": str(url),
            },
            "request": request,
            "vite": vite,
        },
    )
