"""Module that implements a factory method for a FastAPI application."""
import os
import sys
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from kwai.api.v1.auth.api import api_router as auth_api_router
from kwai.api.v1.portal.api import api_router as portal_api_router
from kwai.api.v1.trainings.api import api_router as training_api_router
from kwai.core.dependencies import container
from kwai.core.settings import LoggerSettings, Settings, SettingsException


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Log the start/stop of the application."""
    logger.info("kwai is starting")
    yield
    logger.warning("kwai has ended!")


def configure_logger(settings: LoggerSettings):
    """Configure the logger."""
    try:
        logger.remove(0)  # Remove the default logger
    except ValueError:
        pass

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
        settings.file or sys.stderr,
        format=log_format,
        level=settings.level,
        colorize=True,
        retention=settings.retention,
        rotation=settings.rotation,
        backtrace=False,
        diagnose=False,
    )


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create the FastAPI application.

    Args:
        settings: Settings to use in this application.

    When settings is None (the default), the dependency container will
    load the settings.
    """
    if settings is None:
        try:
            settings = container[Settings]
        except SettingsException as ex:
            logger.error(f"Could not load settings: {ex}")
            sys.exit(0)

    app = FastAPI(title="kwai", lifespan=lifespan)

    # Setup CORS
    if settings.cors:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors.origins,
            allow_credentials=True,
            allow_methods=settings.cors.methods,
            allow_headers=settings.cors.headers,
        )

    # Setup the logger.
    if settings.logger:
        configure_logger(settings.logger)

    app.include_router(auth_api_router, prefix="/api/v1")
    app.include_router(portal_api_router, prefix="/api/v1")
    app.include_router(training_api_router, prefix="/api/v1")

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
