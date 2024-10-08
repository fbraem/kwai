"""Module for starting the api server."""
import argparse

import uvicorn


def create_args():
    """Parse and create cli arguments."""
    parser = argparse.ArgumentParser(description="kwai backend")
    parser.add_argument(
        "--reload",
        action=argparse.BooleanOptionalAction,
        help="Watch for code changes or not",
    )
    parser.add_argument(
        "--host", type=str, default="0.0.0.0", help="The host of the api server."
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="The port of the api server."
    )
    return parser.parse_args()


args = create_args()
uvicorn.run(
    "kwai.api.app:create_app",
    host=args.host,
    port=args.port,
    factory=True,
    reload=args.reload,
)
