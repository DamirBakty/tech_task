from datetime import datetime
from src.domain.entities import Analysis
from src.domain.exceptions import FileNotFoundError
from src.application.repositories import AbstractFileRepository
from src.application.services import AnalysisServiceInterface, AbstractStorageService


class AnalyzeFileUseCase:
    """Use case for analyzing a file using AI."""

    def __init__(
            self,
            file_repository: AbstractFileRepository,
            analysis_service: AnalysisServiceInterface,
            storage_service: AbstractStorageService
    ):
        self.file_repository = file_repository
        self.analysis_service = analysis_service
        self.storage_service = storage_service

    async def execute(self, file_id: int) -> Analysis:
        file = self.file_repository.get_by_id(file_id)
        if file is None:
            raise FileNotFoundError(file_id)

        file_content = await self.storage_service.read(file.path)

        result_text = await self.analysis_service.analyze(file_content, file.original_name)

        analysis = Analysis(
            id=None,
            file_id=file_id,
            status="completed",
            result_text=result_text,
            created_at=datetime.now()
        )

        return self.file_repository.add_analysis(analysis)
