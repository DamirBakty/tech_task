from datetime import datetime
from src.domain.entities import File
from src.application.repositories import AbstractFileRepository
from src.application.services import AbstractStorageService


class UploadFileUseCase:

    def __init__(
            self,
            file_repository: AbstractFileRepository,
            storage_service: AbstractStorageService
    ):
        self.file_repository = file_repository
        self.storage_service = storage_service

    async def execute(
            self,
            original_name: str,
            content: bytes,
            uploaded_by: int = 1
    ) -> File:
        existing_file = self.file_repository.find_latest_by_original_name(original_name)
        version = 1 if existing_file is None else existing_file.version + 1

        storage_path = await self.storage_service.save(original_name, content)

        file = File(
            id=None,
            original_name=original_name,
            path=storage_path,
            version=version,
            size_bytes=len(content),
            uploaded_at=datetime.now(),
            uploaded_by=uploaded_by
        )

        return self.file_repository.add(file)
