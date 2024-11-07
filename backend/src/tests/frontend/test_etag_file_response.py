"""Test the EtagFileResponse."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient
from kwai.frontend.etag_file_response import EtagFileResponse


def test_etag_file_response(tmp_path: Path) -> None:
    """Test the ETag file response."""
    app = FastAPI(title="kwai API -- TEST")

    @app.get("/")
    def get_file():
        return EtagFileResponse(tmp_path / "test_file.txt")

    client = TestClient(app)

    test_file_path = Path(tmp_path / "test_file.txt")
    with open(test_file_path, "w") as f:
        f.write("This is a test file.")

    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["Etag"] is not None

    etag = response.headers["Etag"]
    response = client.get("/", headers={"if-none-match": etag})
    assert response.status_code == 304
