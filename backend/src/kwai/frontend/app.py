"""Module that defines a sub application for handling the frontend."""

import uuid
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from loguru import logger

from kwai.core.settings import Settings, get_settings
from kwai.frontend.apps import apps_router


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

    frontend_app.include_router(apps_router, prefix="/apps")

    @frontend_app.get("/news/{path:path}")
    def news(path: Path, settings: Annotated[Settings, Depends(get_settings)]):
        """Redirect the news path to the portal application.

        When FastAPI serves the frontend, the root path can't be used for the portal.
        So redirect this url to the root application.
        """
        return RedirectResponse(f"/apps/{settings.frontend.root_app}/news/{path}")

    @frontend_app.get("/pages/{path:path}")
    def pages(path: Path, settings: Annotated[Settings, Depends(get_settings)]):
        """Redirect the pages path to the portal application.

        When FastAPI serves the frontend, the root path can't be used for the portal.
        So redirect this url to the root application.
        """
        return RedirectResponse(f"/apps/{settings.frontend.root_app}/pages/{path}")

    @frontend_app.get("/")
    def root(settings: Annotated[Settings, Depends(get_settings)]):
        """Redirect index to the portal application."""
        return RedirectResponse(f"/apps/{settings.frontend.root_app}")

    return frontend_app