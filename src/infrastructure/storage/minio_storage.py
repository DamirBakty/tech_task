import io
import uuid

from minio import Minio
from minio.error import S3Error

from src.config import settings


class MinIOStorage:

    def __init__(self):
        self.client = Minio(
            settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure
        )
        self.bucket_name = settings.minio_bucket_name
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
        except S3Error as e:
            print(f"Error creating bucket: {e}")

    async def save(self, file_name: str, content: bytes) -> str:
        file_extension = file_name.split(".")[-1] if "." in file_name else ""
        unique_key = f"{uuid.uuid4()}"
        if file_extension:
            unique_key = f"{unique_key}.{file_extension}"

        try:
            self.client.put_object(
                self.bucket_name,
                unique_key,
                io.BytesIO(content),
                length=len(content),
                content_type=self._get_content_type(file_name)
            )
            return f"{self.bucket_name}/{unique_key}"
        except S3Error as e:
            raise Exception(f"Failed to upload file to MinIO: {e}")

    async def read(self, path: str) -> bytes:
        try:
            parts = path.split("/", 1)
            if len(parts) != 2:
                raise ValueError(f"Invalid path format: {path}. Expected 'bucket/key'")

            bucket_name, object_key = parts

            response = self.client.get_object(bucket_name, object_key)
            content = response.read()
            response.close()
            response.release_conn()

            return content
        except S3Error as e:
            raise Exception(f"Failed to read file from MinIO: {e}")
        except Exception as e:
            raise Exception(f"Error reading file: {e}")

    @staticmethod
    def _get_content_type(file_name: str) -> str:
        extension = file_name.split(".")[-1].lower() if "." in file_name else ""

        content_types = {
            "pdf": "application/pdf",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "doc": "application/msword",
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "txt": "text/plain",
            "csv": "text/csv",
        }

        return content_types.get(extension, "application/octet-stream")
