"""Module for defining the JSON:API resource for an upload."""

from types import NoneType
from typing import Self

from pydantic import BaseModel

from kwai.api.v1.club.schemas.resources import (
    UploadResourceIdentifier,
)
from kwai.core.json_api import Document, ResourceData, ResourceMeta
from kwai.modules.club.domain.file_upload import FileUploadEntity


class UploadAttributes(BaseModel):
    """Attributes for the upload JSON:API resource."""

    filename: str
    remark: str
    preview: bool


class UploadResource(
    UploadResourceIdentifier, ResourceData[UploadAttributes, NoneType]
):
    """A JSON:API resource for an upload."""


class UploadDocument(Document[UploadResource, NoneType]):
    """A JSON:API document for an upload."""

    @classmethod
    def create(cls, upload: FileUploadEntity) -> Self:
        """Create a document for an upload."""
        upload_resource = UploadResource(
            id=str(upload.uuid),
            attributes=UploadAttributes(
                filename=upload.filename, remark=upload.remark, preview=upload.preview
            ),
            meta=ResourceMeta(
                created_at=str(upload.traceable_time.created_at),
                updated_at=str(upload.traceable_time.updated_at),
            ),
        )

        return cls(data=upload_resource)
