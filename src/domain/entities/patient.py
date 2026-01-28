"""Patient Entity."""
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
from uuid import UUID, uuid4

from ..value_objects.cpf import CPF


@dataclass
class Patient:
    """
    Patient Entity (Aggregate Root).
    
    Represents a patient (elderly person) being cared for.
    """
    
    id: UUID
    caregiver_id: UUID
    full_name: str
    cpf: CPF
    date_of_birth: date
    gender: str  # 'M', 'F', 'Other'
    address: str
    phone: str
    emergency_contact: str
    emergency_phone: str
    medical_conditions: Optional[str] = None
    allergies: Optional[str] = None
    observations: Optional[str] = None
    is_active: bool = True
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    
    @classmethod
    def create(
        cls,
        caregiver_id: UUID,
        full_name: str,
        cpf: str,
        date_of_birth: date,
        gender: str,
        address: str,
        phone: str,
        emergency_contact: str,
        emergency_phone: str,
        medical_conditions: Optional[str] = None,
        allergies: Optional[str] = None,
        observations: Optional[str] = None,
    ) -> "Patient":
        """Factory method to create a new Patient with validation."""
        
        if gender not in ["M", "F", "Other"]:
            raise ValueError(f"Invalid gender: {gender}")
        
        if not full_name or len(full_name) < 3:
            raise ValueError("Full name must have at least 3 characters")
        
        if date_of_birth >= date.today():
            raise ValueError("Date of birth must be in the past")
        
        now = datetime.utcnow()
        
        return cls(
            id=uuid4(),
            caregiver_id=caregiver_id,
            full_name=full_name,
            cpf=CPF(cpf),
            date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            phone=phone,
            emergency_contact=emergency_contact,
            emergency_phone=emergency_phone,
            medical_conditions=medical_conditions,
            allergies=allergies,
            observations=observations,
            is_active=True,
            created_at=now,
            updated_at=now,
        )
    
    def get_age(self) -> int:
        """Calculate patient's age."""
        today = date.today()
        age = today.year - self.date_of_birth.year
        
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        
        return age
    
    def deactivate(self) -> None:
        """Deactivate patient record."""
        if not self.is_active:
            raise ValueError("Patient is already inactive")
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def update_medical_info(
        self,
        medical_conditions: Optional[str] = None,
        allergies: Optional[str] = None,
        observations: Optional[str] = None,
    ) -> None:
        """Update patient's medical information."""
        if medical_conditions is not None:
            self.medical_conditions = medical_conditions
        if allergies is not None:
            self.allergies = allergies
        if observations is not None:
            self.observations = observations
        self.updated_at = datetime.utcnow()
