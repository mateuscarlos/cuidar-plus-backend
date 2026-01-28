"""Appointment Entity."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Appointment:
    """
    Appointment Entity.
    
    Represents a medical appointment for a patient.
    """
    
    id: UUID
    patient_id: UUID
    title: str
    description: Optional[str]
    appointment_date: datetime
    duration_minutes: int
    location: str
    doctor_name: Optional[str] = None
    specialty: Optional[str] = None
    status: str = "scheduled"  # 'scheduled', 'completed', 'cancelled'
    reminder_sent: bool = False
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    
    @classmethod
    def create(
        cls,
        patient_id: UUID,
        title: str,
        appointment_date: datetime,
        duration_minutes: int,
        location: str,
        description: Optional[str] = None,
        doctor_name: Optional[str] = None,
        specialty: Optional[str] = None,
    ) -> "Appointment":
        """Factory method to create a new Appointment with validation."""
        
        if not title or len(title) < 3:
            raise ValueError("Title must have at least 3 characters")
        
        if duration_minutes <= 0:
            raise ValueError("Duration must be greater than 0")
        
        if appointment_date < datetime.utcnow():
            raise ValueError("Appointment date cannot be in the past")
        
        if not location:
            raise ValueError("Location is required")
        
        now = datetime.utcnow()
        
        return cls(
            id=uuid4(),
            patient_id=patient_id,
            title=title,
            description=description,
            appointment_date=appointment_date,
            duration_minutes=duration_minutes,
            location=location,
            doctor_name=doctor_name,
            specialty=specialty,
            status="scheduled",
            reminder_sent=False,
            created_at=now,
            updated_at=now,
        )
    
    def complete(self) -> None:
        """Mark appointment as completed."""
        if self.status == "cancelled":
            raise ValueError("Cannot complete a cancelled appointment")
        if self.status == "completed":
            raise ValueError("Appointment is already completed")
        self.status = "completed"
        self.updated_at = datetime.utcnow()
    
    def cancel(self) -> None:
        """Cancel appointment."""
        if self.status == "completed":
            raise ValueError("Cannot cancel a completed appointment")
        if self.status == "cancelled":
            raise ValueError("Appointment is already cancelled")
        self.status = "cancelled"
        self.updated_at = datetime.utcnow()
    
    def mark_reminder_sent(self) -> None:
        """Mark reminder as sent."""
        self.reminder_sent = True
        self.updated_at = datetime.utcnow()
    
    def reschedule(self, new_date: datetime, new_duration: Optional[int] = None) -> None:
        """Reschedule appointment to a new date."""
        if self.status == "cancelled":
            raise ValueError("Cannot reschedule a cancelled appointment")
        
        if new_date < datetime.utcnow():
            raise ValueError("New appointment date cannot be in the past")
        
        self.appointment_date = new_date
        if new_duration:
            if new_duration <= 0:
                raise ValueError("Duration must be greater than 0")
            self.duration_minutes = new_duration
        
        self.reminder_sent = False
        self.updated_at = datetime.utcnow()
