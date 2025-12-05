from typing import List, Optional, Protocol
from src.domain.entities import File, Analysis


class AbstractFileRepository(Protocol):

    def add(self, file: File) -> File:
        raise NotImplementedError()

    def get_by_id(self, file_id: int) -> Optional[File]:
        raise NotImplementedError()

    def find_latest_by_original_name(self, original_name: str) -> Optional[File]:
        raise NotImplementedError()

    def list_latest_versions(self) -> List[File]:
        raise NotImplementedError()

    def add_analysis(self, analysis: Analysis) -> Analysis:
        raise NotImplementedError()

    def get_analysis_by_file_id(self, file_id: int) -> Optional[Analysis]:
        raise NotImplementedError()
