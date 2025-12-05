from typing import Protocol


class AbstractStorageService(Protocol):
    """Abstract service interface for file storage operations."""

    async def save(self, file_name: str, content: bytes) -> str:
        """
        Save file content to storage.
        
        Args:
            file_name: Name of the file
            content: File content as bytes
            
        Returns:
            Path or identifier where the file was saved
        """
        raise NotImplementedError()

    async def read(self, path: str) -> bytes:
        """
        Read file content from storage.
        
        Args:
            path: Path or identifier of the file in storage
            
        Returns:
            File content as bytes
        """
        raise NotImplementedError()
