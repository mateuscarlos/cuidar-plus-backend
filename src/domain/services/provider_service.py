"""Provider Domain Service - Business Rules."""
from typing import List, Tuple

from ..entities.provider import Provider, ProviderStatus


class ProviderDomainService:
    """
    Domain Service for Provider business rules.
    
    Encapsulates business logic for healthcare providers.
    """
    
    @staticmethod
    def can_be_deactivated(provider: Provider) -> Tuple[bool, str]:
        """
        Check if provider can be deactivated.
        
        Returns:
            Tuple of (can_deactivate, reason)
        """
        if provider.status == ProviderStatus.PENDING_APPROVAL:
            return False, "Prestadora pendente de aprovação não pode ser desativada"
        
        # TODO: Check for active appointments
        # has_active_appointments = check_appointments(provider.id)
        # if has_active_appointments:
        #     return False, "Não pode desativar prestadora com atendimentos agendados"
        
        return True, ""
    
    @staticmethod
    def accepts_insurer(provider: Provider, insurer_id: str) -> bool:
        """Check if provider accepts a specific insurer."""
        from uuid import UUID
        try:
            insurer_uuid = UUID(insurer_id)
            return insurer_uuid in provider.accepted_insurers
        except (ValueError, AttributeError):
            return False
    
    @staticmethod
    def can_add_services(provider: Provider) -> Tuple[bool, str]:
        """Check if provider can add new services."""
        if provider.status != ProviderStatus.ACTIVE:
            return False, "Apenas prestadoras ativas podem adicionar serviços"
        
        return True, ""
    
    @staticmethod
    def has_emergency_service(provider: Provider) -> bool:
        """Check if provider has emergency service."""
        return provider.has_emergency is True
    
    @staticmethod
    def calculate_availability(provider: Provider) -> float:
        """
        Calculate availability percentage based on working hours.
        
        Returns:
            Availability percentage (0-100)
        """
        if not provider.working_hours:
            return 0.0
        
        working_days = sum(
            1 for day in [
                provider.working_hours.monday,
                provider.working_hours.tuesday,
                provider.working_hours.wednesday,
                provider.working_hours.thursday,
                provider.working_hours.friday,
                provider.working_hours.saturday,
                provider.working_hours.sunday,
            ] if day
        )
        
        return (working_days / 7) * 100
    
    @staticmethod
    def has_valid_credentials(provider: Provider) -> bool:
        """Check if provider has valid credentials."""
        if not provider.credentials:
            return False
        
        from datetime import datetime
        
        for credential in provider.credentials:
            if credential.expiration_date:
                if credential.expiration_date < datetime.utcnow():
                    return False
        
        return True
    
    @staticmethod
    def validate_for_creation(
        name: str,
        document: str,
        email: str,
        phone: str,
        specialties: List,
        credentials: List,
    ) -> List[str]:
        """
        Validate provider data before creation.
        
        Returns:
            List of validation errors
        """
        errors = []
        
        # Validate name
        if not name or len(name.strip()) < 3:
            errors.append("Nome da prestadora deve ter no mínimo 3 caracteres")
        
        # Validate document (CPF or CNPJ)
        doc_numbers = ''.join(filter(str.isdigit, document))
        if len(doc_numbers) not in [11, 14]:
            errors.append("Documento inválido - deve ser CPF (11 dígitos) ou CNPJ (14 dígitos)")
        
        # Validate email
        if not email or '@' not in email or '.' not in email.split('@')[1]:
            errors.append("E-mail inválido")
        
        # Validate phone
        phone_numbers = ''.join(filter(str.isdigit, phone))
        if len(phone_numbers) < 10:
            errors.append("Telefone inválido - deve ter no mínimo 10 dígitos")
        
        # Validate specialties
        if not specialties or len(specialties) == 0:
            errors.append("Deve ter pelo menos uma especialidade")
        
        # Validate credentials
        if not credentials or len(credentials) == 0:
            errors.append("Deve ter pelo menos uma credencial (CNES, CRM, etc)")
        
        return errors
    
    @staticmethod
    def validate_document(document: str) -> bool:
        """
        Validate document format (CPF or CNPJ).
        
        Args:
            document: Document string
            
        Returns:
            True if valid format
        """
        doc_numbers = ''.join(filter(str.isdigit, document))
        
        if len(doc_numbers) == 11:
            return ProviderDomainService._validate_cpf(doc_numbers)
        elif len(doc_numbers) == 14:
            return ProviderDomainService._validate_cnpj(doc_numbers)
        
        return False
    
    @staticmethod
    def _validate_cpf(cpf: str) -> bool:
        """Validate CPF check digits."""
        if len(set(cpf)) == 1:
            return False
        
        # First digit
        sum_val = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digit1 = 11 - (sum_val % 11)
        if digit1 >= 10:
            digit1 = 0
        if digit1 != int(cpf[9]):
            return False
        
        # Second digit
        sum_val = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digit2 = 11 - (sum_val % 11)
        if digit2 >= 10:
            digit2 = 0
        if digit2 != int(cpf[10]):
            return False
        
        return True
    
    @staticmethod
    def _validate_cnpj(cnpj: str) -> bool:
        """Validate CNPJ check digits."""
        if len(set(cnpj)) == 1:
            return False
        
        # First digit
        weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum_val = sum(int(cnpj[i]) * weights[i] for i in range(12))
        digit1 = 11 - (sum_val % 11)
        if digit1 >= 10:
            digit1 = 0
        if digit1 != int(cnpj[12]):
            return False
        
        # Second digit
        weights = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum_val = sum(int(cnpj[i]) * weights[i] for i in range(13))
        digit2 = 11 - (sum_val % 11)
        if digit2 >= 10:
            digit2 = 0
        if digit2 != int(cnpj[13]):
            return False
        
        return True
