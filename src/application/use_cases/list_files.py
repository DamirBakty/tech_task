from typing import List
from src.domain.entities import File
from src.application.repositories import AbstractFileRepository


class ListFilesUseCase:

    def __init__(self, file_repository: AbstractFileRepository):
        self.file_repository = file_repository

    def execute(self) -> List[File]:
        return self.file_repository.list_latest_versions()
