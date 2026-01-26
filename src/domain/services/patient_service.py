"""Patient Domain Service - Business Rules."""
from datetime import date, datetime
from typing import List, Tuple, Union

from ..entities.patient import Patient


class PatientDomainService:
    """
    Domain Service for Patient business rules.
    
    Encapsulates business logic for patient management.
    """
    
    @staticmethod
    def calculate_age(birth_date: Union[date, datetime]) -> int:
        """
        Calculate patient age.
        
        Args:
            birth_date: Date of birth (can be date or datetime)
            
        Returns:
            Age in years
        """
        # Convert datetime to date if needed
        if isinstance(birth_date, datetime):
            birth_date = birth_date.date()
        
        today = date.today()
        age = today.year - birth_date.year
        
        # Adjust if birthday hasn't occurred this year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        
        return age
    
    @staticmethod
    def is_pediatric(birth_date: datetime) -> bool:
        """Check if patient is pediatric (under 18)."""
        return PatientDomainService.calculate_age(birth_date) < 18
    
    @staticmethod
    def is_elderly(birth_date: datetime) -> bool:
        """Check if patient is elderly (65 or older)."""
        return PatientDomainService.calculate_age(birth_date) >= 65
    
    @staticmethod
    def requires_companion(patient: Patient) -> bool:
        """
        Check if patient requires a companion.
        
        Companions are required for:
        - Pediatric patients (under 18)
        - Elderly patients (65+)
        - Critical/urgent cases
        
        Args:
            patient: Patient entity
            
        Returns:
            True if companion is required
        """
        age = PatientDomainService.calculate_age(patient.date_of_birth)
        
        # Pediatric or elderly
        if age < 18 or age >= 65:
            return True
        
        # TODO: Check for critical condition when priority is added
        # if patient.priority == PatientPriority.URGENT:
        #     return True
        
        return False
    
    @staticmethod
    def can_be_discharged(patient: Patient) -> Tuple[bool, str]:
        """
        Check if patient can be discharged.
        
        Returns:
            Tuple of (can_discharge, reason)
        """
        if not patient.is_active:
            return False, "Paciente já foi dado alta"
        
        # TODO: Add more business rules
        # - Check for pending treatments
        # - Check for unpaid bills
        # - Check for required documents
        
        return True, ""
    
    @staticmethod
    def validate_for_creation(
        full_name: str,
        cpf: str,
        date_of_birth: datetime,
        phone: str,
        emergency_phone: str,
    ) -> List[str]:
        """
        Validate patient data before creation.
        
        Returns:
            List of validation errors
        """
        errors = []
        
        # Validate name
        if not full_name or len(full_name.strip()) < 3:
            errors.append("Nome deve ter pelo menos 3 caracteres")
        
        # Validate CPF format (basic)
        cpf_numbers = ''.join(filter(str.isdigit, cpf))
        if len(cpf_numbers) != 11:
            errors.append("CPF deve conter 11 dígitos")
        
        # Validate date of birth
        if date_of_birth >= datetime.utcnow():
            errors.append("Data de nascimento não pode ser futura")
        
        # Check if too old (reasonable limit)
        age = PatientDomainService.calculate_age(date_of_birth)
        if age > 120:
            errors.append("Data de nascimento inválida")
        
        # Validate phone
        phone_numbers = ''.join(filter(str.isdigit, phone))
        if len(phone_numbers) < 10:
            errors.append("Telefone de contato inválido")
        
        # Validate emergency phone
        emergency_numbers = ''.join(filter(str.isdigit, emergency_phone))
        if len(emergency_numbers) < 10:
            errors.append("Telefone de emergência inválido")
        
        return errors
    
    @staticmethod
    def validate_cpf(cpf: str) -> bool:
        """
        Validate CPF check digits.
        
        Args:
            cpf: CPF string (with or without formatting)
            
        Returns:
            True if valid, False otherwise
        """
        cpf = ''.join(filter(str.isdigit, cpf))
        
        if len(cpf) != 11:
            return False
        
        # Check if all digits are the same
        if len(set(cpf)) == 1:
            return False
        
        # Validate first digit
        sum_val = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digit1 = 11 - (sum_val % 11)
        if digit1 >= 10:
            digit1 = 0
        if digit1 != int(cpf[9]):
            return False
        
        # Validate second digit
        sum_val = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digit2 = 11 - (sum_val % 11)
        if digit2 >= 10:
            digit2 = 0
        if digit2 != int(cpf[10]):
            return False
        
        return True
    
    @staticmethod
    def format_cpf(cpf: str) -> str:
        """
        Format CPF with mask.
        
        Args:
            cpf: CPF string
            
        Returns:
            Formatted CPF (XXX.XXX.XXX-XX)
        """
        cpf = ''.join(filter(str.isdigit, cpf))
        if len(cpf) != 11:
            return cpf
        
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    
    @staticmethod
    def get_risk_level(patient: Patient) -> str:
        """
        Calculate patient risk level based on age and conditions.
        
        Args:
            patient: Patient entity
            
        Returns:
            Risk level: 'LOW', 'MEDIUM', 'HIGH'
        """
        age = PatientDomainService.calculate_age(patient.date_of_birth)
        
        # High risk: elderly with medical conditions
        if age >= 65 and patient.medical_conditions:
            return "HIGH"
        
        # Medium risk: elderly or has conditions
        if age >= 65 or patient.medical_conditions:
            return "MEDIUM"
        
        # Low risk: young and healthy
        return "LOW"
