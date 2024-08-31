"""Module that defines a sub application for handling the frontend."""

import uuid
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

    @frontend_app.get("/")
    def root(settings: Annotated[Settings, Depends(get_settings)]):
        return RedirectResponse(f"/apps/{settings.frontend.root_app}")

    return frontend_app
