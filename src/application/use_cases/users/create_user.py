"""Create User Use Case."""
from dataclasses import dataclass
from uuid import UUID

from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.domain.value_objects.email import Email
from src.infrastructure.security.password_hasher import PasswordHasher
from src.shared.exceptions.application_exception import ApplicationException


@dataclass
class CreateUserInput:
    """Input DTO for CreateUser use case."""
    email: str
    password: str
    full_name: str
    role: str


@dataclass
class CreateUserOutput:
    """Output DTO for CreateUser use case."""
    id: UUID
    email: str
    full_name: str
    role: str
    is_active: bool


class CreateUserUseCase:
    """
    Use Case: Create a new user.
    
    Orchestrates the user creation process following business rules.
    """
    
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher
    
    def execute(self, input_dto: CreateUserInput) -> CreateUserOutput:
        """
        Execute the use case.
        
        Steps:
        1. Validate email uniqueness
        2. Hash password
        3. Create user entity
        4. Persist user
        5. Return output DTO
        """
        
        # Validate email uniqueness
        email = Email(input_dto.email)
        if self._user_repository.exists_by_email(email):
            raise ApplicationException(
                message="User with this email already exists",
                code="USER_ALREADY_EXISTS",
            )
        
        # Hash password
        password_hash = self._password_hasher.hash(input_dto.password)
        
        # Create user entity (business rules applied here)
        user = User.create(
            email=input_dto.email,
            password_hash=password_hash,
            full_name=input_dto.full_name,
            role=input_dto.role,
        )
        
        # Persist user
        saved_user = self._user_repository.save(user)
        
        # Return output DTO
        return CreateUserOutput(
            id=saved_user.id,
            email=str(saved_user.email),
            full_name=saved_user.full_name,
            role=saved_user.role,
            is_active=saved_user.is_active,
        )
