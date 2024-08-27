"""Module that creates a FastAPI application for the API and Frontend."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from kwai.api.app import create_api
from kwai.frontend.app import create_frontend

APP_NAME = "kwai"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Log the start/stop of the application."""
    logger.info(f"{APP_NAME} is starting")
    yield
    logger.warning(f"{APP_NAME} has ended!")


def create_app() -> FastAPI:
    """Create the FastAPI application for API and frontend."""
    main_app = FastAPI(title=APP_NAME, lifespan=lifespan)
    api_app = create_api()
    main_app.mount("/api", api_app)

    frontend_app = create_frontend()
    main_app.mount("/", frontend_app)

    return main_app
