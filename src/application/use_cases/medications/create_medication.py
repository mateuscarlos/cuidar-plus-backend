"""Create Medication Use Case."""
from dataclasses import dataclass
from datetime import datetime, time
from typing import Optional
from uuid import UUID

from src.domain.entities.medication import Medication
from src.domain.repositories.medication_repository import MedicationRepository
from src.domain.repositories.patient_repository import PatientRepository
from src.domain.services.medication_scheduler import MedicationScheduler
from src.shared.exceptions.application_exception import ApplicationException


@dataclass
class CreateMedicationInput:
    """Input DTO for CreateMedication use case."""
    patient_id: UUID
    name: str
    dosage: str
    frequency: str
    schedule_times: list[time]
    start_date: datetime
    end_date: Optional[datetime] = None
    instructions: Optional[str] = None


@dataclass
class CreateMedicationOutput:
    """Output DTO for CreateMedication use case."""
    id: UUID
    patient_id: UUID
    name: str
    dosage: str
    frequency: str
    warnings: list[str]


class CreateMedicationUseCase:
    """
    Use Case: Create a new medication for a patient.
    """
    
    def __init__(
        self,
        medication_repository: MedicationRepository,
        patient_repository: PatientRepository,
        medication_scheduler: MedicationScheduler,
    ) -> None:
        self._medication_repository = medication_repository
        self._patient_repository = patient_repository
        self._medication_scheduler = medication_scheduler
    
    def execute(self, input_dto: CreateMedicationInput) -> CreateMedicationOutput:
        """
        Execute the use case.
        
        Steps:
        1. Validate patient exists
        2. Check for medication conflicts
        3. Create medication entity
        4. Persist medication
        5. Return output with warnings
        """
        
        # Validate patient exists
        patient = self._patient_repository.find_by_id(input_dto.patient_id)
        if not patient:
            raise ApplicationException(
                message=f"Patient with ID {input_dto.patient_id} not found",
                code="PATIENT_NOT_FOUND",
            )
        
        # Create medication entity
        medication = Medication.create(
            patient_id=input_dto.patient_id,
            name=input_dto.name,
            dosage=input_dto.dosage,
            frequency=input_dto.frequency,
            schedule_times=input_dto.schedule_times,
            start_date=input_dto.start_date,
            end_date=input_dto.end_date,
            instructions=input_dto.instructions,
        )
        
        # Check for conflicts
        existing_medications = self._medication_repository.find_active_by_patient(
            input_dto.patient_id
        )
        warnings = self._medication_scheduler.check_medication_conflict(
            existing_medications, medication
        )
        
        # Persist medication
        saved_medication = self._medication_repository.save(medication)
        
        # Return output
        return CreateMedicationOutput(
            id=saved_medication.id,
            patient_id=saved_medication.patient_id,
            name=saved_medication.name,
            dosage=saved_medication.dosage,
            frequency=saved_medication.frequency,
            warnings=warnings,
        )
