"""Medication Scheduler Domain Service."""
from datetime import datetime, time, timedelta
from typing import List
from uuid import UUID

from ..entities.medication import Medication


class MedicationScheduler:
    """
    Domain Service for medication scheduling logic.
    
    This service contains business logic that doesn't naturally fit
    within a single entity.
    """
    
    @staticmethod
    def generate_daily_schedule(
        medications: List[Medication],
        date: datetime
    ) -> List[dict]:
        """
        Generate a daily medication schedule for a patient.
        
        Returns a list of medication doses for the specified date,
        sorted by time.
        """
        schedule = []
        
        for medication in medications:
            if not medication.is_active:
                continue
            
            # Check if medication should be taken on this date
            if medication.start_date.date() > date.date():
                continue
            
            if medication.end_date and medication.end_date.date() < date.date():
                continue
            
            # Add each scheduled time for this medication
            for schedule_time in medication.schedule_times:
                scheduled_datetime = datetime.combine(date.date(), schedule_time)
                
                schedule.append({
                    "medication_id": medication.id,
                    "medication_name": medication.name,
                    "dosage": medication.dosage,
                    "scheduled_time": scheduled_datetime,
                    "instructions": medication.instructions,
                    "taken": False,
                })
        
        # Sort by time
        schedule.sort(key=lambda x: x["scheduled_time"])
        
        return schedule
    
    @staticmethod
    def get_next_dose(medication: Medication) -> datetime:
        """
        Get the next scheduled dose time for a medication.
        """
        now = datetime.now()
        today = now.date()
        
        # Find the next scheduled time today
        for schedule_time in sorted(medication.schedule_times):
            scheduled_datetime = datetime.combine(today, schedule_time)
            if scheduled_datetime > now:
                return scheduled_datetime
        
        # If no more doses today, return first dose tomorrow
        tomorrow = today + timedelta(days=1)
        first_time = min(medication.schedule_times)
        return datetime.combine(tomorrow, first_time)
    
    @staticmethod
    def check_medication_conflict(
        existing_medications: List[Medication],
        new_medication: Medication
    ) -> List[str]:
        """
        Check for potential conflicts between medications.
        
        Returns a list of warning messages if conflicts are found.
        """
        warnings = []
        
        for existing in existing_medications:
            if not existing.is_active:
                continue
            
            # Check if medication names are too similar (potential duplicate)
            if existing.name.lower() == new_medication.name.lower():
                warnings.append(
                    f"Patient is already taking medication with the same name: {existing.name}"
                )
            
            # Check for overlapping schedules (too many medications at same time)
            overlapping_times = set(existing.schedule_times) & set(new_medication.schedule_times)
            if len(overlapping_times) > 0:
                warnings.append(
                    f"Schedule overlaps with {existing.name} at times: "
                    f"{', '.join(str(t) for t in overlapping_times)}"
                )
        
        return warnings
