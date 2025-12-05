from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from src.infrastructure.persistence.database import Base


class FileModel(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    original_name = Column(String, nullable=False, index=True)
    path = Column(String, nullable=False)
    version = Column(Integer, nullable=False, default=1)
    size_bytes = Column(Integer, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.now, nullable=False)
    uploaded_by = Column(Integer, nullable=False, default=1)

    analyses = relationship("AnalysisModel", back_populates="file")


class AnalysisModel(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False, index=True)
    status = Column(String, nullable=False, default="pending")
    result_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    file = relationship("FileModel", back_populates="analyses")
