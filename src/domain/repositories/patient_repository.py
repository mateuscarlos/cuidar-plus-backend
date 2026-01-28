"""Patient Repository Interface."""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ..entities.patient import Patient


class PatientRepository(ABC):
    """
    Patient Repository Interface (Port).
    
    Defines the contract for patient persistence operations.
    """
    
    @abstractmethod
    def save(self, patient: Patient) -> Patient:
        """Persist a patient entity."""
        pass
    
    @abstractmethod
    def find_by_id(self, patient_id: UUID) -> Optional[Patient]:
        """Find patient by ID."""
        pass
    
    @abstractmethod
    def find_by_caregiver(self, caregiver_id: UUID) -> list[Patient]:
        """Find all patients for a specific caregiver."""
        pass
    
    @abstractmethod
    def delete(self, patient_id: UUID) -> None:
        """Delete patient by ID."""
        pass
    
    @abstractmethod
    def find_all(self, skip: int = 0, limit: int = 100) -> list[Patient]:
        """Find all patients with pagination."""
        pass
