"""Module that defines a file upload entity."""
from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.traceable_time import TraceableTime

FileUploadIdentifier = IntIdentifier


class FileUploadEntity(Entity[FileUploadIdentifier]):
    """An FileUploadEntity keeps information about a file upload."""

    def __init__(
        self,
        *,
        id_: FileUploadIdentifier | None = None,
        filename: str,
        owner: Owner,
        remark: str = "",
        traceable_time: TraceableTime | None = None,
    ):
        """Initialize a file upload entity.

        Args:
            id_: The id of the upload.
            filename: The name of the file.
            remark: A remark about the upload.
            owner: The user who uploaded the file.
            traceable_time: The creation and modification timestamp of the upload.
        """
        super().__init__(id_ or FileUploadIdentifier())
        self._filename = filename
        self._owner = owner
        self._remark = remark
        self._traceable_time = traceable_time or TraceableTime()

    @property
    def filename(self) -> str:
        """Return the filename."""
        return self._filename

    @property
    def remark(self) -> str:
        """Return the remark."""
        return self._remark

    @property
    def owner(self) -> Owner:
        """Return the owner."""
        return self._owner

    @property
    def traceable_time(self) -> TraceableTime:
        """Return the creation/modification time."""
        return self._traceable_time
