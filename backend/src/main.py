import sys

from loguru import logger
import uvicorn

from kwai.app import create_app
from kwai.core.settings import get_settings, SettingsException

try:
    settings = get_settings()
except SettingsException as se:
    logger.error(f"Could not load the settings: {se}!")
    sys.exit(1)


if __name__ == "__main__":
    uvicorn.run(create_app(settings), host="0.0.0.0", port=8000)
else:
    app = create_app(settings)
