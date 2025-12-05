from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, UploadFile, File as FastAPIFile, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.domain.exceptions import FileNotFoundError, AnalysisNotFoundError
from src.infrastructure.api.dependencies import (
    get_upload_file_use_case,
    get_list_files_use_case,
    get_analyze_file_use_case,
    get_get_analysis_use_case
)
from src.infrastructure.persistence.database import get_db

router = APIRouter(prefix="/files", tags=["files"])


class FileResponse(BaseModel):
    """Response schema for file information."""
    id: int
    original_name: str
    version: int
    uploaded_at: datetime
    size_bytes: int

    class Config:
        from_attributes = True


class AnalysisResponse(BaseModel):
    """Response schema for analysis results."""
    id: int
    file_id: int
    status: str
    result_text: str | None
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("/upload", response_model=FileResponse, status_code=201)
async def upload_file(
        file: UploadFile = FastAPIFile(...),
        db: Session = Depends(get_db)
):
    """
    Upload a file with automatic versioning.

    - Accepts any file format (PDF, DOCX, PNG, etc.)
    - Automatically increments version if file with same name exists
    - Stores file in MinIO
    - Records metadata in database
    """
    use_case = get_upload_file_use_case(db)

    content = await file.read()

    created_file = await use_case.execute(
        original_name=file.filename,
        content=content,
        uploaded_by=1
    )

    return FileResponse(
        id=created_file.id,
        original_name=created_file.original_name,
        version=created_file.version,
        uploaded_at=created_file.uploaded_at,
        size_bytes=created_file.size_bytes
    )


@router.get("", response_model=List[FileResponse])
def list_files(db: Session = Depends(get_db)):
    use_case = get_list_files_use_case(db)
    files = use_case.execute()

    return [
        FileResponse(
            id=f.id,
            original_name=f.original_name,
            version=f.version,
            uploaded_at=f.uploaded_at,
            size_bytes=f.size_bytes
        )
        for f in files
    ]


@router.post("/{file_id}/analyze", response_model=AnalysisResponse, status_code=201)
async def analyze_file(
        file_id: int,
        db: Session = Depends(get_db)
):
    use_case = get_analyze_file_use_case(db)

    try:
        analysis = await use_case.execute(file_id)

        return AnalysisResponse(
            id=analysis.id,
            file_id=analysis.file_id,
            status=analysis.status,
            result_text=analysis.result_text,
            created_at=analysis.created_at
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{file_id}/analysis", response_model=AnalysisResponse)
def get_analysis(
        file_id: int,
        db: Session = Depends(get_db)
):
    use_case = get_get_analysis_use_case(db)

    try:
        analysis = use_case.execute(file_id)

        return AnalysisResponse(
            id=analysis.id,
            file_id=analysis.file_id,
            status=analysis.status,
            result_text=analysis.result_text,
            created_at=analysis.created_at
        )
    except (FileNotFoundError, AnalysisNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
