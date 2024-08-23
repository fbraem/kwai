"""Module that defines a sub application for handling the frontend."""

import uuid
from enum import Enum
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger

from kwai.api.dependencies import create_templates
from kwai.core.settings import Settings, get_settings
from kwai.frontend.vite import DevelopmentVite, ProductionVite


class FrontendApplicationName(str, Enum):
    """Defines all available frontend application names."""

    portal = "portal"
    coach = "coach"

    @classmethod
    def list(cls):
        """List all available frontend application names."""
        return [c.value for c in cls]


def create_frontend_app(frontend_app: FastAPI, settings: Settings, application: str):
    """Create a frontend for an application."""
    # Public files
    root_path = Path(settings.frontend.path) / "apps" / application / "dist"
    frontend_app.mount(f"/apps/{application}/public", StaticFiles(directory=root_path))
    # Assets
    frontend_app.mount(
        f"/apps/{application}/assets", StaticFiles(directory=root_path / "assets")
    )

    @frontend_app.get("/apps/{app}/{router:path}")
    async def get_app(
        request: Request,
        templates: Annotated[Jinja2Templates, Depends(create_templates)],
        app: FrontendApplicationName,
    ):
        """Get the html page for a given frontend application.

        Remark: the router:path is required for handling a refresh on a vue-router page.
        """
        manifest_path = root_path / "manifest.json"
        if not manifest_path.exists():
            raise HTTPException(
                status_code=status.INTERNAL_SERVER_ERROR,
                detail=f"Manifest file {manifest_path} not found",
            )

        if not hasattr(settings.frontend.apps, app):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Application {app} does not exist.",
            )

        app_setting = getattr(settings.frontend.apps, app)

        if settings.frontend.test:
            if app_setting.base_dev is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Setting base_dev not set for application {app}",
                )
            vite = DevelopmentVite(app_setting.base_dev)
        else:
            vite = ProductionVite(manifest_path, app_setting.base)

        return templates.TemplateResponse(
            "index.jinja2",
            {
                "request": request,
                "settings": settings,
                "vite": vite,
            },
        )


def create_frontend():
    """Create the frontend."""
    frontend_app = FastAPI()

    @frontend_app.get("/")
    async def get_root(settings: Annotated[Settings, Depends(get_settings)]):
        """Redirect the root path to the portal application."""
        return RedirectResponse(f"/apps/{settings.frontend.root_app}")

    @frontend_app.middleware("http")
    async def log(request: Request, call_next):
        """Middleware for logging the requests."""
        request_id = str(uuid.uuid4())
        with logger.contextualize(request_id=request_id):
            logger.info(f"{request.url} - {request.method} - Request started")

            response = None  # Make pylint happy...
            try:
                response = await call_next(request)
            except Exception as ex:
                logger.error(f"{request.url} - Request failed: {ex}")
                logger.exception(ex)
                response = JSONResponse(
                    content={
                        "detail": str(ex),
                    },
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            finally:
                response.headers["X-Request-ID"] = request_id
                logger.info(
                    f"{request.url} - {request.method} - Request ended: "
                    f"{response.status_code}"
                )

            return response

    kwai_settings = get_settings()
    for application in FrontendApplicationName.list():
        create_frontend_app(frontend_app, kwai_settings, application)

    return frontend_app
