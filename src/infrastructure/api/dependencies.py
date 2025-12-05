from sqlalchemy.orm import Session
from src.infrastructure.persistence.database import get_db
from src.infrastructure.persistence.repositories import SQLAlchemyFileRepository
from src.infrastructure.services import MockAIAnalyzer, OpenAIAnalyzer
from src.infrastructure.storage import MinIOStorage
from src.application.use_cases import (
    UploadFileUseCase,
    ListFilesUseCase,
    AnalyzeFileUseCase,
    GetAnalysisUseCase,
)
from src.application.services import AnalysisServiceInterface
from src.config import settings


def get_file_repository(db: Session = None) -> SQLAlchemyFileRepository:
    if db is None:
        db = next(get_db())
    return SQLAlchemyFileRepository(db)


def get_storage_service() -> MinIOStorage:
    return MinIOStorage()


def get_analysis_service() -> AnalysisServiceInterface:
    if settings.use_mock_analyzer:
        return MockAIAnalyzer()
    else:
        return OpenAIAnalyzer()


def get_upload_file_use_case(db: Session) -> UploadFileUseCase:
    file_repository = get_file_repository(db)
    storage_service = get_storage_service()
    return UploadFileUseCase(file_repository, storage_service)


def get_list_files_use_case(db: Session) -> ListFilesUseCase:
    file_repository = get_file_repository(db)
    return ListFilesUseCase(file_repository)


def get_analyze_file_use_case(db: Session) -> AnalyzeFileUseCase:
    file_repository = get_file_repository(db)
    analysis_service = get_analysis_service()
    storage_service = get_storage_service()
    return AnalyzeFileUseCase(file_repository, analysis_service, storage_service)


def get_get_analysis_use_case(db: Session) -> GetAnalysisUseCase:
    file_repository = get_file_repository(db)
    return GetAnalysisUseCase(file_repository)
