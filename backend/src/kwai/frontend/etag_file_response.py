"""Module that implements an etag response for a file."""

from hashlib import md5
from pathlib import Path

from fastapi import Request
from fastapi.responses import FileResponse, Response


class EtagFileResponse(FileResponse):
    """A FileResponse that will check the etag when if-none-match header is passed.

    _generate_etag uses the same implementation as FileResponse.
    FileResponse automatically sets the etag header with this etag value.
    """

    def __init__(self, path: Path, **kwargs) -> None:
        super().__init__(path, **kwargs)
        self._path = path

    def _generate_etag(self) -> str:
        file_stat = self._path.stat()
        etag_base = str(file_stat.st_mtime) + "-" + str(file_stat.st_size)
        return f'"{md5(etag_base.encode(), usedforsecurity=False)}"'

    async def __call__(self, scope, receive, send) -> None:
        """Check the etag, and return 304 when the file is not modified."""
        request = Request(scope, receive)
        if_none_match = request.headers.get("if-none-match")

        if not if_none_match:
            await super().__call__(scope, receive, send)
            return

        etag = self._generate_etag()
        if if_none_match == etag:
            response = Response(status_code=304)
            await response(scope, receive, send)
            return

        await super().__call__(scope, receive, send)
