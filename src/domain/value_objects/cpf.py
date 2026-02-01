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
        
        # Convert to integers once
        digits = [int(d) for d in cpf]

        # Validate first check digit
        # Calculate sum for first digit and sum of first 9 digits simultaneously
        sum1 = 0
        sum_digits_0_8 = 0
        for i in range(9):
            val = digits[i]
            sum1 += val * (10 - i)
            sum_digits_0_8 += val

        first_digit = (sum1 * 10 % 11) % 10
        
        if digits[9] != first_digit:
            return False
        
        # Validate second check digit
        # Optimization: Reuse sum1 and sum_digits_0_8
        # sum2 = sum(d[i] * (11-i)) for i in 0..9
        #      = sum(d[i] * (10-i) + d[i]) for i in 0..8 + d[9]*2
        #      = sum1 + sum_digits_0_8 + d[9]*2
        sum2 = sum1 + sum_digits_0_8 + digits[9] * 2
        second_digit = (sum2 * 10 % 11) % 10
        
        if digits[10] != second_digit:
            return False
        
        return True
    
    def formatted(self) -> str:
        """Return formatted CPF (XXX.XXX.XXX-XX)."""
        return f"{self.value[:3]}.{self.value[3:6]}.{self.value[6:9]}-{self.value[9:]}"
    
    def __str__(self) -> str:
        return self.formatted()
    
    def __repr__(self) -> str:
        return f"CPF('{self.formatted()}')"
