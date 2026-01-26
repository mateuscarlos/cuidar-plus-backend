"""Email Service Interface."""
from abc import ABC, abstractmethod
from typing import List, Optional


class EmailService(ABC):
    """
    Email Service Interface (Port).
    
    Infrastructure layer will implement this interface.
    """
    
    @abstractmethod
    def send_email(
        self,
        to: List[str],
        subject: str,
        body: str,
        html: Optional[str] = None,
    ) -> bool:
        """Send an email."""
        pass
    
    @abstractmethod
    def send_template_email(
        self,
        to: List[str],
        template_name: str,
        context: dict,
    ) -> bool:
        """Send an email using a template."""
        pass
