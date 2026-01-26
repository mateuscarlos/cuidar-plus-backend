"""Unit tests for CPF value object."""
import pytest

from src.domain.value_objects.cpf import CPF


class TestCPFValueObject:
    """Test suite for CPF value object."""
    
    def test_create_valid_cpf(self):
        """Test creating a valid CPF."""
        # Valid CPF: 111.444.777-35
        cpf = CPF("11144477735")
        
        assert cpf.value == "11144477735"
        assert cpf.formatted() == "111.444.777-35"
    
    def test_create_cpf_with_formatting(self):
        """Test creating CPF with formatting characters."""
        cpf = CPF("111.444.777-35")
        
        assert cpf.value == "11144477735"
        assert cpf.formatted() == "111.444.777-35"
    
    def test_create_invalid_cpf_wrong_length(self):
        """Test creating CPF with wrong length raises ValueError."""
        with pytest.raises(ValueError, match="Invalid CPF"):
            CPF("123456789")
    
    def test_create_invalid_cpf_all_same_digits(self):
        """Test creating CPF with all same digits raises ValueError."""
        with pytest.raises(ValueError, match="Invalid CPF"):
            CPF("11111111111")
    
    def test_create_invalid_cpf_wrong_checksum(self):
        """Test creating CPF with invalid checksum raises ValueError."""
        with pytest.raises(ValueError, match="Invalid CPF"):
            CPF("12345678901")  # Invalid checksum
    
    def test_cpf_immutability(self):
        """Test that CPF value object is immutable."""
        cpf = CPF("11144477735")
        
        # Should not be able to change value
        with pytest.raises(AttributeError):
            cpf.value = "00000000000"
