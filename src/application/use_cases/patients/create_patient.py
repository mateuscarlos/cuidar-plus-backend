"""Create Patient Use Case."""
from dataclasses import dataclass
from datetime import date
from typing import Optional
from uuid import UUID

from src.domain.entities.patient import Patient
from src.domain.repositories.patient_repository import PatientRepository
from src.domain.repositories.user_repository import UserRepository
from src.shared.exceptions.application_exception import ApplicationException


@dataclass
class CreatePatientInput:
    """Input DTO for CreatePatient use case."""
    caregiver_id: UUID
    full_name: str
    cpf: str
    date_of_birth: date
    gender: str
    address: str
    phone: str
    emergency_contact: str
    emergency_phone: str
    medical_conditions: Optional[str] = None
    allergies: Optional[str] = None
    observations: Optional[str] = None


@dataclass
class CreatePatientOutput:
    """Output DTO for CreatePatient use case."""
    id: UUID
    caregiver_id: UUID
    full_name: str
    cpf: str
    age: int
    gender: str


class CreatePatientUseCase:
    """
    Use Case: Create a new patient.
    """
    
    def __init__(
        self,
        patient_repository: PatientRepository,
        user_repository: UserRepository,
    ) -> None:
        self._patient_repository = patient_repository
        self._user_repository = user_repository
    
    def execute(self, input_dto: CreatePatientInput) -> CreatePatientOutput:
        """
        Execute the use case.
        
        Steps:
        1. Validate caregiver exists
        2. Create patient entity
        3. Persist patient
        4. Return output DTO
        """
        
        # Validate caregiver exists
        caregiver = self._user_repository.find_by_id(input_dto.caregiver_id)
        if not caregiver:
            raise ApplicationException(
                message=f"Caregiver with ID {input_dto.caregiver_id} not found",
                code="CAREGIVER_NOT_FOUND",
            )
        
        # Create patient entity
        patient = Patient.create(
            caregiver_id=input_dto.caregiver_id,
            full_name=input_dto.full_name,
            cpf=input_dto.cpf,
            date_of_birth=input_dto.date_of_birth,
            gender=input_dto.gender,
            address=input_dto.address,
            phone=input_dto.phone,
            emergency_contact=input_dto.emergency_contact,
            emergency_phone=input_dto.emergency_phone,
            medical_conditions=input_dto.medical_conditions,
            allergies=input_dto.allergies,
            observations=input_dto.observations,
        )
        
        # Persist patient
        saved_patient = self._patient_repository.save(patient)
        
        # Return output DTO
        return CreatePatientOutput(
            id=saved_patient.id,
            caregiver_id=saved_patient.caregiver_id,
            full_name=saved_patient.full_name,
            cpf=str(saved_patient.cpf),
            age=saved_patient.get_age(),
            gender=saved_patient.gender,
        )
