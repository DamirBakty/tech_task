from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class File:
    """Domain entity representing a file with versioning."""
    id: Optional[int]
    original_name: str
    path: str
    version: int
    size_bytes: int
    uploaded_at: datetime
    uploaded_by: int
    analysis_id: Optional[int] = None


@dataclass
class Analysis:
    """Domain entity representing an AI analysis result."""
    id: Optional[int]
    file_id: int
    status: str
    result_text: Optional[str]
    created_at: datetime
