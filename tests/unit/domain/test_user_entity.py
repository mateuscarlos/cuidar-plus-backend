"""Unit tests for User entity."""
import pytest
from datetime import datetime

from src.domain.entities.user import User
from src.domain.value_objects.email import Email


class TestUserEntity:
    """Test suite for User entity."""
    
    def test_create_user_successfully(self):
        """Test creating a valid user."""
        # Arrange & Act
        user = User.create(
            email="test@example.com",
            password_hash="hashed_password",
            full_name="Test User",
            role="caregiver",
        )
        
        # Assert
        assert user.id is not None
        assert user.email.value == "test@example.com"
        assert user.password_hash == "hashed_password"
        assert user.full_name == "Test User"
        assert user.role == "caregiver"
        assert user.is_active is True
        assert user.created_at is not None
        assert user.updated_at is not None
        assert user.last_login is None
    
    def test_create_user_with_invalid_role(self):
        """Test creating user with invalid role raises ValueError."""
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid role"):
            User.create(
                email="test@example.com",
                password_hash="hashed_password",
                full_name="Test User",
                role="invalid_role",
            )
    
    def test_create_user_with_short_name(self):
        """Test creating user with too short name raises ValueError."""
        # Act & Assert
        with pytest.raises(ValueError, match="at least 3 characters"):
            User.create(
                email="test@example.com",
                password_hash="hashed_password",
                full_name="AB",
                role="caregiver",
            )
    
    def test_deactivate_user(self):
        """Test deactivating a user."""
        # Arrange
        user = User.create(
            email="test@example.com",
            password_hash="hashed_password",
            full_name="Test User",
            role="caregiver",
        )
        
        # Act
        user.deactivate()
        
        # Assert
        assert user.is_active is False
    
    def test_deactivate_already_inactive_user(self):
        """Test deactivating an already inactive user raises ValueError."""
        # Arrange
        user = User.create(
            email="test@example.com",
            password_hash="hashed_password",
            full_name="Test User",
            role="caregiver",
        )
        user.deactivate()
        
        # Act & Assert
        with pytest.raises(ValueError, match="already inactive"):
            user.deactivate()
    
    def test_update_last_login(self):
        """Test updating last login timestamp."""
        # Arrange
        user = User.create(
            email="test@example.com",
            password_hash="hashed_password",
            full_name="Test User",
            role="caregiver",
        )
        
        # Act
        user.update_last_login()
        
        # Assert
        assert user.last_login is not None
        assert isinstance(user.last_login, datetime)
