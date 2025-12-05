from src.domain.entities import Analysis
from src.domain.exceptions import AnalysisNotFoundError, FileNotFoundError
from src.application.repositories import AbstractFileRepository


class GetAnalysisUseCase:

    def __init__(self, file_repository: AbstractFileRepository):
        self.file_repository = file_repository

    def execute(self, file_id: int) -> Analysis:
        file = self.file_repository.get_by_id(file_id)
        if file is None:
            raise FileNotFoundError(file_id)

        analysis = self.file_repository.get_analysis_by_file_id(file_id)
        if analysis is None:
            raise AnalysisNotFoundError(file_id)

        return analysis
