"""Module for starting the api server."""
import sys

import uvicorn
from loguru import logger

from kwai.app import create_app
from kwai.core.dependencies import container
from kwai.core.settings import Settings, SettingsException

if __name__ == "__main__":
    try:
        settings = container[Settings]
    except SettingsException as se:
        logger.error(f"Could not load settings: {se}")
        sys.exit(0)

    uvicorn.run(create_app(settings), host="0.0.0.0", port=8000)
