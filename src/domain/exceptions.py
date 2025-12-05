class BaseAppException(Exception):
    pass


class FileNotFoundError(BaseAppException):
    def __init__(self, file_id: int):
        self.file_id = file_id
        super().__init__(f"File with id {file_id} not found")


class AnalysisNotFoundError(BaseAppException):
    def __init__(self, file_id: int):
        self.file_id = file_id
        super().__init__(f"Analysis not found for file with id {file_id}")
