"""Appointment Repository Interface."""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from uuid import UUID

from ..entities.appointment import Appointment


class AppointmentRepository(ABC):
    """
    Appointment Repository Interface (Port).
    
    Defines the contract for appointment persistence operations.
    """
    
    @abstractmethod
    def save(self, appointment: Appointment) -> Appointment:
        """Persist an appointment entity."""
        pass
    
    @abstractmethod
    def find_by_id(self, appointment_id: UUID) -> Optional[Appointment]:
        """Find appointment by ID."""
        pass
    
    @abstractmethod
    def find_by_patient(self, patient_id: UUID) -> list[Appointment]:
        """Find all appointments for a specific patient."""
        pass
    
    @abstractmethod
    def find_upcoming_by_patient(self, patient_id: UUID) -> list[Appointment]:
        """Find upcoming appointments for a specific patient."""
        pass
    
    @abstractmethod
    def find_by_date_range(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> list[Appointment]:
        """Find appointments within a date range."""
        pass
    
    @abstractmethod
    def delete(self, appointment_id: UUID) -> None:
        """Delete appointment by ID."""
        pass
