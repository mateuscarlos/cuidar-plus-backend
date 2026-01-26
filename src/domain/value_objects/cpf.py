"""CPF Value Object."""
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class CPF:
    """
    CPF (Brazilian Individual Taxpayer ID) Value Object.
    
    Immutable value object that ensures CPF validity.
    """
    
    value: str
    
    def __post_init__(self) -> None:
        """Validate CPF format and checksum on initialization."""
        cleaned = self._clean_cpf(self.value)
        if not self._is_valid_cpf(cleaned):
            raise ValueError(f"Invalid CPF: {self.value}")
        
        # Store the cleaned version
        object.__setattr__(self, 'value', cleaned)
    
    @staticmethod
    def _clean_cpf(cpf: str) -> str:
        """Remove non-numeric characters from CPF."""
        return re.sub(r'\D', '', cpf)
    
    @staticmethod
    def _is_valid_cpf(cpf: str) -> bool:
        """
        Validate CPF using the official algorithm.
        
        CPF format: XXX.XXX.XXX-XX (11 digits)
        """
        # Check if CPF has 11 digits
        if len(cpf) != 11:
            return False
        
        # Check if all digits are the same (invalid CPF)
        if cpf == cpf[0] * 11:
            return False
        
        # Validate first check digit
        sum_digits = sum(int(cpf[i]) * (10 - i) for i in range(9))
        first_digit = (sum_digits * 10 % 11) % 10
        
        if int(cpf[9]) != first_digit:
            return False
        
        # Validate second check digit
        sum_digits = sum(int(cpf[i]) * (11 - i) for i in range(10))
        second_digit = (sum_digits * 10 % 11) % 10
        
        if int(cpf[10]) != second_digit:
            return False
        
        return True
    
    def formatted(self) -> str:
        """Return formatted CPF (XXX.XXX.XXX-XX)."""
        return f"{self.value[:3]}.{self.value[3:6]}.{self.value[6:9]}-{self.value[9:]}"
    
    def __str__(self) -> str:
        return self.formatted()
    
    def __repr__(self) -> str:
        return f"CPF('{self.formatted()}')"
