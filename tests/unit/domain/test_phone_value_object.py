"""Unit tests for Phone value object."""
import pytest

from src.domain.value_objects.phone import Phone


class TestPhoneValueObject:
    """Test suite for Phone value object."""

    def test_create_valid_mobile_phone(self):
        """Test creating a valid mobile phone."""
        # Valid mobile: (11) 98765-4321
        phone = Phone("11987654321")

        assert phone.value == "11987654321"
        assert phone.formatted() == "(11) 98765-4321"

    def test_create_valid_landline_phone(self):
        """Test creating a valid landline phone."""
        # Valid landline: (11) 3333-4444
        phone = Phone("1133334444")

        assert phone.value == "1133334444"
        assert phone.formatted() == "(11) 3333-4444"

    def test_create_phone_with_formatting(self):
        """Test creating Phone with formatting characters."""
        phone = Phone("(11) 98765-4321")

        assert phone.value == "11987654321"
        assert phone.formatted() == "(11) 98765-4321"

    def test_create_phone_with_weird_characters(self):
        """Test creating Phone with weird characters which should be cleaned."""
        # Should fail if country code is included (13 digits)
        with pytest.raises(ValueError):
            Phone("+55 (11) 98765-4321")

        # Standard input without country code but with symbols
        phone = Phone("(11) 98765-4321")
        assert phone.value == "11987654321"

    def test_create_invalid_phone_wrong_length(self):
        """Test creating Phone with wrong length raises ValueError."""
        with pytest.raises(ValueError, match="Invalid phone number"):
            Phone("123456789") # 9 digits

    def test_create_invalid_mobile_without_9(self):
        """Test creating mobile phone (11 digits) without 9 as third digit."""
        with pytest.raises(ValueError, match="Invalid phone number"):
            Phone("11887654321") # 11 digits, but 3rd is 8

    def test_phone_immutability(self):
        """Test that Phone value object is immutable."""
        phone = Phone("11987654321")

        # Should not be able to change value
        with pytest.raises(AttributeError):
            phone.value = "00000000000"
