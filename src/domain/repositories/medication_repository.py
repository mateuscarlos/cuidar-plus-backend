"""Medication Repository Interface."""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ..entities.medication import Medication


class MedicationRepository(ABC):
    """
    Medication Repository Interface (Port).
    
    Defines the contract for medication persistence operations.
    """
    
    @abstractmethod
    def save(self, medication: Medication) -> Medication:
        """Persist a medication entity."""
        pass
    
    @abstractmethod
    def find_by_id(self, medication_id: UUID) -> Optional[Medication]:
        """Find medication by ID."""
        pass
    
    @abstractmethod
    def find_by_patient(self, patient_id: UUID) -> list[Medication]:
        """Find all medications for a specific patient."""
        pass
    
    @abstractmethod
    def find_active_by_patient(self, patient_id: UUID) -> list[Medication]:
        """Find all active medications for a specific patient."""
        pass
    
    @abstractmethod
    def delete(self, medication_id: UUID) -> None:
        """Delete medication by ID."""
        pass
