"""Unit tests for Email value object."""
import pytest

from src.domain.value_objects.email import Email


class TestEmailValueObject:
    """Test suite for Email value object."""
    
    def test_create_valid_email(self):
        """Test creating a valid email."""
        # Arrange & Act
        email = Email("test@example.com")
        
        # Assert
        assert email.value == "test@example.com"
        assert str(email) == "test@example.com"
    
    def test_create_invalid_email_format(self):
        """Test creating email with invalid format raises ValueError."""
        invalid_emails = [
            "invalid",
            "invalid@",
            "@example.com",
            "invalid@.com",
            "invalid @example.com",
            "",
        ]
        
        for invalid_email in invalid_emails:
            with pytest.raises(ValueError, match="Invalid email format"):
                Email(invalid_email)
    
    def test_email_immutability(self):
        """Test that email value object is immutable."""
        # Arrange
        email = Email("test@example.com")
        
        # Act & Assert
        with pytest.raises(AttributeError):
            email.value = "new@example.com"
