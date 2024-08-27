"""Module for starting the api server.

This will only start the api server. Use this when the frontend is not served
by FastAPI or if the api server is running on another server.
"""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from loguru import logger

from kwai.core.args import create_args

APP_NAME = "kwai API"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Log the start/stop of the API application.

    Remark: This will only be executed when kwai API is the main application.
    """
    logger.info(f"{APP_NAME} is starting")
    yield
    logger.warning(f"{APP_NAME} has ended!")


api_app = FastAPI(title="kwai API", lifespan=lifespan)


args = create_args(APP_NAME)
uvicorn.run(
    api_app,
    host=args.host,
    port=args.port,
    reload=args.reload,
)
