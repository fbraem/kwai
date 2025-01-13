"""Module for starting kwai.

When this module is used, it will start the api and frontend application.
If only the api is required, use kwai.api.
"""

import uvicorn

from kwai.app import APP_NAME
from kwai.core.args import create_args


args = create_args(APP_NAME)
uvicorn.run(
    "kwai.app:create_app",
    host=args.host,
    port=args.port,
    factory=True,
    reload=args.reload,
)
