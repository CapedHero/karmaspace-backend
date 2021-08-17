from typing import Any, IO, Optional

from django.core.files.storage import FileSystemStorage

from storages.backends.s3boto3 import S3Boto3Storage


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = "media"


class OverwriteFileSystemStorage(FileSystemStorage):
    def _save(self, name: str, content: IO[Any]) -> Any:
        self.delete(name)
        return super()._save(name, content)

    def get_available_name(self, name: str, max_length: Optional[int] = None) -> str:
        return name
