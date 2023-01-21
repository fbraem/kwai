import sys

from loguru import logger
import uvicorn

from kwai.app import create_app
from kwai.core.dependencies import container
from kwai.core.settings import Settings

settings = container[Settings]

if __name__ == "__main__":
    uvicorn.run(create_app(settings), host="0.0.0.0", port=8000)
else:
    app = create_app(settings)
