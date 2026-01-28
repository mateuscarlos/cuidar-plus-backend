"""User Repository Interface."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ..entities.user import User
from ..value_objects.email import Email


class UserRepository(ABC):
    """
    User Repository Interface (Port).
    
    Defines the contract for user persistence operations.
    Infrastructure layer will implement this interface.
    """
    
    @abstractmethod
    def save(self, user: User) -> User:
        """Persist a user entity."""
        pass
    
    @abstractmethod
    def find_by_id(self, user_id: UUID) -> Optional[User]:
        """Find user by ID."""
        pass
    
    @abstractmethod
    def find_by_email(self, email: Email) -> Optional[User]:
        """Find user by email."""
        pass
    
    @abstractmethod
    def exists_by_email(self, email: Email) -> bool:
        """Check if user exists by email."""
        pass
    
    @abstractmethod
    def delete(self, user_id: UUID) -> None:
        """Delete user by ID."""
        pass
    
    @abstractmethod
    def find_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Find all users with pagination."""
        pass
