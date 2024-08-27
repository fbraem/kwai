"""Module for starting kwai.

When this module is used, it will start the api and frontend application.
If only the api is required, use kwai.api.
"""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from loguru import logger

from kwai.api.app import create_app
from kwai.core.args import create_args
from kwai.frontend.app import create_frontend

APP_NAME = "kwai"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Log the start/stop of the application."""
    logger.info(f"{APP_NAME} is starting")
    yield
    logger.warning(f"{APP_NAME} has ended!")


main_app = FastAPI(title=APP_NAME, lifespan=lifespan)
api_app = create_app()
main_app.mount("/api", api_app)

frontend_app = create_frontend()
main_app.mount("/", frontend_app)

args = create_args(APP_NAME)
uvicorn.run(
    main_app,
    host=args.host,
    port=args.port,
    reload=args.reload,
)
