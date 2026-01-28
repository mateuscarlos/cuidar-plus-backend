"""Insurer Domain Service - Business Rules."""
from typing import List

from ..entities.insurer import Insurer, InsurerStatus


class InsurerDomainService:
    """
    Domain Service for Insurer business rules.
    
    Encapsulates business logic that doesn't naturally fit within a single entity.
    """
    
    @staticmethod
    def can_be_deactivated(insurer: Insurer) -> tuple[bool, str]:
        """
        Check if insurer can be deactivated.
        
        Returns:
            Tuple of (can_deactivate, reason)
        """
        has_active_plans = any(plan.active for plan in insurer.plans)
        
        if has_active_plans:
            return False, "Não pode desativar operadora com planos ativos"
        
        return True, ""
    
    @staticmethod
    def can_add_plans(insurer: Insurer) -> tuple[bool, str]:
        """Check if insurer can have new plans added."""
        if insurer.status != InsurerStatus.ACTIVE:
            return False, "Apenas operadoras ativas podem adicionar planos"
        
        return True, ""
    
    @staticmethod
    def validate_for_creation(
        name: str,
        cnpj: str,
        registration_number: str,
        email: str,
        phone: str,
    ) -> List[str]:
        """
        Validate insurer data before creation.
        
        Returns:
            List of validation errors
        """
        errors = []
        
        # Validate name
        if not name or len(name.strip()) < 3:
            errors.append("Nome da operadora deve ter no mínimo 3 caracteres")
        
        # Validate CNPJ
        cnpj_numbers = ''.join(filter(str.isdigit, cnpj))
        if len(cnpj_numbers) != 14:
            errors.append("CNPJ inválido - deve conter 14 dígitos")
        
        # Validate ANS registration
        reg_numbers = ''.join(filter(str.isdigit, registration_number))
        if len(reg_numbers) != 6:
            errors.append("Número de registro ANS inválido - deve ter 6 dígitos")
        
        # Validate email
        if not email or '@' not in email or '.' not in email.split('@')[1]:
            errors.append("E-mail inválido")
        
        # Validate phone
        phone_numbers = ''.join(filter(str.isdigit, phone))
        if len(phone_numbers) < 10:
            errors.append("Telefone inválido - deve ter no mínimo 10 dígitos")
        
        return errors
    
    @staticmethod
    def validate_cnpj(cnpj: str) -> bool:
        """
        Validate CNPJ format and check digits.
        
        Args:
            cnpj: CNPJ string (with or without formatting)
            
        Returns:
            True if valid, False otherwise
        """
        cnpj = ''.join(filter(str.isdigit, cnpj))
        
        if len(cnpj) != 14:
            return False
        
        # Check if all digits are the same
        if len(set(cnpj)) == 1:
            return False
        
        # Validate first check digit
        sum_val = 0
        weight = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        for i in range(12):
            sum_val += int(cnpj[i]) * weight[i]
        
        digit1 = 11 - (sum_val % 11)
        if digit1 >= 10:
            digit1 = 0
        
        if digit1 != int(cnpj[12]):
            return False
        
        # Validate second check digit
        sum_val = 0
        weight = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        for i in range(13):
            sum_val += int(cnpj[i]) * weight[i]
        
        digit2 = 11 - (sum_val % 11)
        if digit2 >= 10:
            digit2 = 0
        
        if digit2 != int(cnpj[13]):
            return False
        
        return True
