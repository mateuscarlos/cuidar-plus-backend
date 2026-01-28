"""Medication Entity."""
from dataclasses import dataclass
from datetime import datetime, time
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Medication:
    """
    Medication Entity.
    
    Represents a medication that a patient needs to take.
    """
    
    id: UUID
    patient_id: UUID
    name: str
    dosage: str
    frequency: str  # 'daily', 'twice_daily', 'three_times_daily', 'as_needed'
    schedule_times: list[time]  # List of times to take medication
    start_date: datetime
    end_date: Optional[datetime] = None
    instructions: Optional[str] = None
    is_active: bool = True
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    
    @classmethod
    def create(
        cls,
        patient_id: UUID,
        name: str,
        dosage: str,
        frequency: str,
        schedule_times: list[time],
        start_date: datetime,
        end_date: Optional[datetime] = None,
        instructions: Optional[str] = None,
    ) -> "Medication":
        """Factory method to create a new Medication with validation."""
        
        valid_frequencies = ["daily", "twice_daily", "three_times_daily", "as_needed"]
        if frequency not in valid_frequencies:
            raise ValueError(f"Invalid frequency: {frequency}. Must be one of {valid_frequencies}")
        
        if not name or len(name) < 2:
            raise ValueError("Medication name must have at least 2 characters")
        
        if not dosage:
            raise ValueError("Dosage is required")
        
        if not schedule_times:
            raise ValueError("At least one schedule time is required")
        
        if end_date and end_date < start_date:
            raise ValueError("End date cannot be before start date")
        
        now = datetime.utcnow()
        
        return cls(
            id=uuid4(),
            patient_id=patient_id,
            name=name,
            dosage=dosage,
            frequency=frequency,
            schedule_times=schedule_times,
            start_date=start_date,
            end_date=end_date,
            instructions=instructions,
            is_active=True,
            created_at=now,
            updated_at=now,
        )
    
    def deactivate(self) -> None:
        """Deactivate medication."""
        if not self.is_active:
            raise ValueError("Medication is already inactive")
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def update_schedule(self, schedule_times: list[time]) -> None:
        """Update medication schedule times."""
        if not schedule_times:
            raise ValueError("At least one schedule time is required")
        self.schedule_times = schedule_times
        self.updated_at = datetime.utcnow()
