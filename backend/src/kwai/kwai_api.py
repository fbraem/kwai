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
        "--port", type=int, default=8000, help="The port of the api server."
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = create_args()
    uvicorn.run(
        "kwai.api.app:create_app",
        host="0.0.0.0",
        port=args.port,
        factory=True,
        reload=args.reload,
    )
