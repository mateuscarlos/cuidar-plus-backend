"""Email Value Object."""
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    """
    Email Value Object.
    
    Immutable value object that ensures email validity.
    """
    
    value: str
    
    def __post_init__(self) -> None:
        """Validate email format on initialization."""
        if not self._is_valid_email(self.value):
            raise ValueError(f"Invalid email format: {self.value}")
    
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Validate email using regex pattern."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"Email('{self.value}')"
