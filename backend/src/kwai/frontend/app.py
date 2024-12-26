"""Module that defines a sub application for handling the frontend."""

import uuid
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from loguru import logger

from kwai.core.settings import Settings, get_settings
from kwai.frontend.apps import application_routers


def get_default_app(settings: Annotated[Settings, Depends(get_settings)]) -> str:
    """Search for the default application in the settings."""
    for app in settings.frontend.apps:
        if app.default:
            return app.name
    raise ValueError("No default app defined in settings.")


def create_frontend():
    """Create the frontend."""
    frontend_app = FastAPI()

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

    for router in application_routers:
        frontend_app.include_router(router, prefix="/apps")

    @frontend_app.get("/favicon.ico", include_in_schema=False)
    def favicon() -> FileResponse:
        """Return the favicon."""
        favicon_path = Path(__file__).parent.parent / "static" / "favicon.ico"
        if favicon_path.is_file():
            return FileResponse(favicon_path)
        raise status.HTTP_404_NOT_FOUND

    @frontend_app.get("/news/{path:path}", name="frontend.news")
    def news(path: Path, default_app: Annotated[str, Depends(get_default_app)]):
        """Redirect the news path to the portal application.

        When FastAPI serves the frontend, the root path can't be used for the portal.
        So redirect this url to the root application.
        """
        return RedirectResponse(f"/apps/{default_app}/news/{path}")

    @frontend_app.get("/pages/{path:path}", name="frontend.pages")
    def pages(path: Path, default_app: Annotated[str, Depends(get_default_app)]):
        """Redirect the pages path to the portal application.

        When FastAPI serves the frontend, the root path can't be used for the portal.
        So redirect this url to the root application.
        """
        return RedirectResponse(f"/apps/{default_app}/pages/{path}")

    @frontend_app.get("/", name="frontend.home")
    def root(default_app: Annotated[str, Depends(get_default_app)]):
        """Redirect index to the portal application."""
        return RedirectResponse(f"/apps/{default_app}")

    return frontend_app
