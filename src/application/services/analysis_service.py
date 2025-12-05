from typing import Protocol

class AnalysisServiceInterface(Protocol):
    """Abstract service interface for AI analysis."""
    
    async def analyze(self, file_content: bytes, file_name: str) -> str:
        """
        Analyze file content and return a text result.
        
        Args:
            file_content: File content as bytes
            file_name: Name of the file
            
        Returns:
            Analysis result as text
        """
        raise NotImplementedError()
