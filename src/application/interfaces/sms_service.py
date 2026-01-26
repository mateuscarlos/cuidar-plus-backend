"""SMS Service Interface."""
from abc import ABC, abstractmethod


class SMSService(ABC):
    """
    SMS Service Interface (Port).
    
    Infrastructure layer will implement this interface.
    """
    
    @abstractmethod
    def send_sms(self, to: str, message: str) -> bool:
        """Send an SMS message."""
        pass
