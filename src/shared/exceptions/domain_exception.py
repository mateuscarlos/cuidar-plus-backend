"""Domain Exception - Base exception for domain layer."""


class DomainException(Exception):
    """
    Base exception for domain-level errors.
    
    Use this for business rule violations that happen in the domain layer.
    """
    
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return self.message
