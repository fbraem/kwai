import os
import sys
import uuid

from loguru import logger
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from kwai.api.v1.auth.api import api_router
from kwai.core.settings import get_settings, SettingsException

settings = None
try:
    settings = get_settings()
except SettingsException as se:
    logger.error(f"Could not load the settings: {se}!")
    exit(1)


# Setup the logger.
if settings.logger:
    logger.remove(0)  # Remove the default logger

    def log_format(record):
        """Change the format when a request_id is set in extra."""
        if "request_id" in record["extra"]:
            return "{time} - {level} - ({extra[request_id]}) - {message}" + os.linesep
        return "{time} - {level} - {message}" + os.linesep

    logger.add(
        settings.logger.file or sys.stderr,
        format=log_format,
        level=settings.logger.level,
        colorize=True,
        retention=settings.logger.retention,
        rotation=settings.logger.rotation,
    )


def startup():
    logger.info("KWAI is starting")


def shutdown():
    logger.warning("KWAI has ended!")


app = FastAPI(on_startup=[startup], on_shutdown=[shutdown])

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

        try:
            response = await call_next(request)
        except Exception as ex:
            logger.error(f"{request.url} - Request failed: {ex}")
            response = JSONResponse(
                content={
                    "detail": str(ex),
                },
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        finally:
            response.headers["X-Request-ID"] = request_id
            logger.info(
                f"{request.url} - {request.method } - Request ended: {response.status_code}"
            )

        return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
