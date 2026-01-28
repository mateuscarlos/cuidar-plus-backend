"""Get User By ID Use Case."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.domain.repositories.user_repository import UserRepository
from src.shared.exceptions.application_exception import ApplicationException


@dataclass
class GetUserByIdOutput:
    """Output DTO for GetUserById use case."""
    id: UUID
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]


class GetUserByIdUseCase:
    """
    Use Case: Get user by ID.
    """
    
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository
    
    def execute(self, user_id: UUID) -> GetUserByIdOutput:
        """
        Execute the use case.
        
        Steps:
        1. Find user by ID
        2. Return user data
        """
        
        user = self._user_repository.find_by_id(user_id)
        
        if not user:
            raise ApplicationException(
                message=f"User with ID {user_id} not found",
                code="USER_NOT_FOUND",
            )
        
        return GetUserByIdOutput(
            id=user.id,
            email=str(user.email),
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
            last_login=user.last_login,
        )
