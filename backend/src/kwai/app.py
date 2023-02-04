"""Module that implements a factory method for a FastAPI application."""
import os
import sys
import uuid

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from kwai.api.v1.auth.api import api_router
from kwai.core.dependencies import container
from kwai.core.settings import Settings, SettingsException


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create the FastAPI application.

    When settings is None (the default), the dependency container will
    load the settings.

    :parameter settings: Settings to use in this application.
    """
    if settings is None:
        try:
            settings = container[Settings]
        except SettingsException as ex:
            logger.error(f"Could not load settings: {ex}")
            sys.exit(0)

    def startup():
        logger.info("KWAI is starting")

    def shutdown():
        logger.warning("KWAI has ended!")

    app = FastAPI(on_startup=[startup], on_shutdown=[shutdown])

    # Setup the logger.
    if settings.logger:
        logger.remove(0)  # Remove the default logger

        def log_format(record):
            """Change the format when a request_id is set in extra."""
            if "request_id" in record["extra"]:
                new_format = (
                    "{time} - {level} - ({extra[request_id]}) - {message}" + os.linesep
                )
            else:
                new_format = "{time} - {level} - {message}" + os.linesep
            if record["exception"]:
                new_format += "{exception}" + os.linesep
            return new_format

        logger.add(
            settings.logger.file or sys.stderr,
            format=log_format,
            level=settings.logger.level,
            colorize=True,
            retention=settings.logger.retention,
            rotation=settings.logger.rotation,
            backtrace=False,
            diagnose=False,
        )

    if len(settings.security.cors_origin) > 0:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.security.cors_origin,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(api_router, prefix="/api/v1")

    @app.middleware("http")
    async def log(request: Request, call_next):
        """Middleware for logging the requests."""
        request_id = str(uuid.uuid4())
        with logger.contextualize(request_id=request_id):
            logger.info(f"{request.url} - {request.method} - Request started")

            response = None  # Make pylint happy...
            try:
                response = await call_next(request)
            except Exception as ex:  # pylint: disable=W0703
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
                    f"{request.url} - {request.method } - Request ended: "
                    f"{response.status_code}"
                )

            return response

    return app
