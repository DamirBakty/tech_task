from typing import List, Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.domain.entities import File, Analysis
from src.infrastructure.persistence.models import FileModel, AnalysisModel


class SQLAlchemyFileRepository:

    def __init__(self, session: Session):
        self.session = session

    def add(self, file: File) -> File:
        file_model = FileModel(
            original_name=file.original_name,
            path=file.path,
            version=file.version,
            size_bytes=file.size_bytes,
            uploaded_at=file.uploaded_at,
            uploaded_by=file.uploaded_by
        )
        self.session.add(file_model)
        self.session.commit()
        self.session.refresh(file_model)

        return self._to_entity(file_model)

    def get_by_id(self, file_id: int) -> Optional[File]:
        file_model = self.session.query(FileModel).filter(FileModel.id == file_id).first()
        return self._to_entity(file_model) if file_model else None

    def find_latest_by_original_name(self, original_name: str) -> Optional[File]:
        file_model = (
            self.session.query(FileModel)
            .filter(FileModel.original_name == original_name)
            .order_by(desc(FileModel.version))
            .first()
        )
        return self._to_entity(file_model) if file_model else None

    def list_latest_versions(self) -> List[File]:
        subquery = (
            self.session.query(
                FileModel.original_name,
                desc(FileModel.version).label("max_version")
            )
            .group_by(FileModel.original_name)
            .subquery()
        )

        files = (
            self.session.query(FileModel)
            .join(
                subquery,
                (FileModel.original_name == subquery.c.original_name) &
                (FileModel.version == subquery.c.max_version)
            )
            .all()
        )

        return [self._to_entity(f) for f in files]

    def add_analysis(self, analysis: Analysis) -> Analysis:
        analysis_model = AnalysisModel(
            file_id=analysis.file_id,
            status=analysis.status,
            result_text=analysis.result_text,
            created_at=analysis.created_at
        )
        self.session.add(analysis_model)
        self.session.commit()
        self.session.refresh(analysis_model)

        return self._analysis_to_entity(analysis_model)

    def get_analysis_by_file_id(self, file_id: int) -> Optional[Analysis]:
        analysis_model = (
            self.session.query(AnalysisModel)
            .filter(AnalysisModel.file_id == file_id)
            .order_by(desc(AnalysisModel.created_at))
            .first()
        )
        return self._analysis_to_entity(analysis_model) if analysis_model else None

    @staticmethod
    def _to_entity(model: FileModel) -> File:
        return File(
            id=model.id,
            original_name=model.original_name,
            path=model.path,
            version=model.version,
            size_bytes=model.size_bytes,
            uploaded_at=model.uploaded_at,
            uploaded_by=model.uploaded_by
        )

    @staticmethod
    def _analysis_to_entity(model: AnalysisModel) -> Analysis:
        return Analysis(
            id=model.id,
            file_id=model.file_id,
            status=model.status,
            result_text=model.result_text,
            created_at=model.created_at
        )
