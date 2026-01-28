"""Authenticate User Use Case."""
from dataclasses import dataclass
from typing import Optional

from src.domain.repositories.user_repository import UserRepository
from src.domain.value_objects.email import Email
from src.infrastructure.security.password_hasher import PasswordHasher
from src.infrastructure.security.jwt_handler import JWTHandler
from src.shared.exceptions.application_exception import ApplicationException


@dataclass
class AuthenticateUserInput:
    """Input DTO for AuthenticateUser use case."""
    email: str
    password: str


@dataclass
class AuthenticateUserOutput:
    """Output DTO for AuthenticateUser use case."""
    access_token: str
    refresh_token: Optional[str]
    token_type: str
    expires_in: int


class AuthenticateUserUseCase:
    """
    Use Case: Authenticate a user and generate JWT tokens.
    """
    
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        jwt_handler: JWTHandler,
    ) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._jwt_handler = jwt_handler
    
    def execute(self, input_dto: AuthenticateUserInput) -> AuthenticateUserOutput:
        """
        Execute the use case.
        
        Steps:
        1. Find user by email
        2. Verify password
        3. Check if user is active
        4. Generate JWT tokens
        5. Update last login
        6. Return tokens
        """
        
        # Find user by email
        email = Email(input_dto.email)
        user = self._user_repository.find_by_email(email)
        
        if not user:
            raise ApplicationException(
                message="Invalid email or password",
                code="INVALID_CREDENTIALS",
            )
        
        # Verify password
        if not self._password_hasher.verify(input_dto.password, user.password_hash):
            raise ApplicationException(
                message="Invalid email or password",
                code="INVALID_CREDENTIALS",
            )
        
        # Check if user is active
        if not user.is_active:
            raise ApplicationException(
                message="User account is inactive",
                code="INACTIVE_USER",
            )
        
        # Generate JWT tokens
        access_token = self._jwt_handler.create_access_token(
            subject=str(user.id),
            additional_claims={"email": str(user.email), "role": user.role}
        )
        
        refresh_token = self._jwt_handler.create_refresh_token(subject=str(user.id))
        
        # Update last login
        user.update_last_login()
        self._user_repository.save(user)
        
        # Return tokens
        return AuthenticateUserOutput(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
            expires_in=self._jwt_handler.access_token_expires,
        )
