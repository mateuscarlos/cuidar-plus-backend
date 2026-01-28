"""Application Exception - Base exception for application layer."""


class ApplicationException(Exception):
    """
    Base exception for application-level errors.
    
    Use this for use case failures and application logic errors.
    """
    
    def __init__(self, message: str, code: str = "APPLICATION_ERROR") -> None:
        self.message = message
        self.code = code
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"
