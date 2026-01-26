"""SQLAlchemy User Repository Implementation."""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.domain.value_objects.email import Email
from src.infrastructure.database.models.user_model import UserModel


class SQLAlchemyUserRepository(UserRepository):
    """
    SQLAlchemy implementation of UserRepository.
    
    Adapts domain entities to database models.
    """
    
    def __init__(self, session: Session) -> None:
        self._session = session
    
    def save(self, user: User) -> User:
        """Persist user to database."""
        user_model = self._to_model(user)
        self._session.merge(user_model)
        self._session.flush()
        return self._to_entity(user_model)
    
    def find_by_id(self, user_id: UUID) -> Optional[User]:
        """Find user by ID."""
        user_model = self._session.query(UserModel).filter(
            UserModel.id == user_id
        ).first()
        
        return self._to_entity(user_model) if user_model else None
    
    def find_by_email(self, email: Email) -> Optional[User]:
        """Find user by email."""
        user_model = self._session.query(UserModel).filter(
            UserModel.email == str(email)
        ).first()
        
        return self._to_entity(user_model) if user_model else None
    
    def exists_by_email(self, email: Email) -> bool:
        """Check if user exists by email."""
        return self._session.query(UserModel).filter(
            UserModel.email == str(email)
        ).count() > 0
    
    def delete(self, user_id: UUID) -> None:
        """Delete user by ID."""
        self._session.query(UserModel).filter(
            UserModel.id == user_id
        ).delete()
    
    def find_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Find all users with pagination."""
        user_models = self._session.query(UserModel).offset(skip).limit(limit).all()
        return [self._to_entity(model) for model in user_models]
    
    @staticmethod
    def _to_model(user: User) -> UserModel:
        """Convert domain entity to database model."""
        return UserModel(
            id=user.id,
            email=str(user.email),
            password_hash=user.password_hash,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login,
        )
    
    @staticmethod
    def _to_entity(model: UserModel) -> User:
        """Convert database model to domain entity."""
        return User(
            id=model.id,
            email=Email(model.email),
            password_hash=model.password_hash,
            full_name=model.full_name,
            role=model.role,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
            last_login=model.last_login,
        )
