"""User Entity - Aggregate Root."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from ..value_objects.email import Email


@dataclass
class User:
    """
    User Entity (Aggregate Root).
    
    Represents a user in the system following DDD principles.
    This entity contains business rules and invariants.
    """
    
    id: UUID
    email: Email
    password_hash: str
    full_name: str
    role: str  # 'caregiver', 'family', 'admin'
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    
    @classmethod
    def create(
        cls,
        email: str,
        password_hash: str,
        full_name: str,
        role: str,
    ) -> "User":
        """Factory method to create a new User with validation."""
        
        if role not in ["caregiver", "family", "admin"]:
            raise ValueError(f"Invalid role: {role}")
        
        if not full_name or len(full_name) < 3:
            raise ValueError("Full name must have at least 3 characters")
        
        now = datetime.utcnow()
        
        return cls(
            id=uuid4(),
            email=Email(email),
            password_hash=password_hash,
            full_name=full_name,
            role=role,
            is_active=True,
            created_at=now,
            updated_at=now,
            last_login=None,
        )
    
    def deactivate(self) -> None:
        """Business rule: Deactivate user account."""
        if not self.is_active:
            raise ValueError("User is already inactive")
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def activate(self) -> None:
        """Business rule: Activate user account."""
        if self.is_active:
            raise ValueError("User is already active")
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def update_last_login(self) -> None:
        """Update last login timestamp."""
        self.last_login = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def change_password(self, new_password_hash: str) -> None:
        """Change user password."""
        if not new_password_hash:
            raise ValueError("Password hash cannot be empty")
        self.password_hash = new_password_hash
        self.updated_at = datetime.utcnow()
