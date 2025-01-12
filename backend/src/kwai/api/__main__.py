"""Module for starting the api server.

This will only start the api server. Use this when the frontend is not served
by FastAPI or if the api server is running on another server.
"""

import uvicorn

from kwai.api.app import APP_NAME
from kwai.core.args import create_args

args = create_args(APP_NAME)
uvicorn.run(
    "kwai.api.app.create_api",
    host=args.host,
    port=args.port,
    factory=True,
    reload=args.reload,
)
