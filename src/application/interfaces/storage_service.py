"""Storage Service Interface."""
from abc import ABC, abstractmethod
from typing import Optional


class StorageService(ABC):
    """
    Storage Service Interface (Port).
    
    Infrastructure layer will implement this interface (e.g., S3, local storage).
    """
    
    @abstractmethod
    def upload_file(
        self,
        file_path: str,
        content: bytes,
        content_type: Optional[str] = None,
    ) -> str:
        """
        Upload a file and return the URL.
        
        Args:
            file_path: The path/key where the file should be stored
            content: The file content as bytes
            content_type: MIME type of the file
        
        Returns:
            URL to access the uploaded file
        """
        pass
    
    @abstractmethod
    def download_file(self, file_path: str) -> bytes:
        """Download a file and return its content."""
        pass
    
    @abstractmethod
    def delete_file(self, file_path: str) -> bool:
        """Delete a file."""
        pass
    
    @abstractmethod
    def file_exists(self, file_path: str) -> bool:
        """Check if a file exists."""
        pass
