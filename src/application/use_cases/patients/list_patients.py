"""List Patients Use Case."""
from dataclasses import dataclass
from uuid import UUID

from src.domain.repositories.patient_repository import PatientRepository


@dataclass
class PatientSummary:
    """Summary DTO for a patient."""
    id: UUID
    full_name: str
    age: int
    gender: str
    is_active: bool


@dataclass
class ListPatientsOutput:
    """Output DTO for ListPatients use case."""
    patients: list[PatientSummary]
    total: int


class ListPatientsByCaregiverUseCase:
    """
    Use Case: List all patients for a specific caregiver.
    """
    
    def __init__(self, patient_repository: PatientRepository) -> None:
        self._patient_repository = patient_repository
    
    def execute(self, caregiver_id: UUID) -> ListPatientsOutput:
        """
        Execute the use case.
        
        Steps:
        1. Find all patients for caregiver
        2. Map to summary DTOs
        3. Return output
        """
        
        patients = self._patient_repository.find_by_caregiver(caregiver_id)
        
        patient_summaries = [
            PatientSummary(
                id=patient.id,
                full_name=patient.full_name,
                age=patient.get_age(),
                gender=patient.gender,
                is_active=patient.is_active,
            )
            for patient in patients
        ]
        
        return ListPatientsOutput(
            patients=patient_summaries,
            total=len(patient_summaries),
        )
