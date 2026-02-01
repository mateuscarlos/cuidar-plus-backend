"""Medication SQLAlchemy Model."""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import ARRAY, JSON, Boolean, Column, DateTime, ForeignKey, String, Text, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..session import Base


class MedicationModel(Base):
    """SQLAlchemy model for Medication entity."""

    __tablename__ = "medications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    dosage = Column(String(100), nullable=False)
    frequency = Column(String(50), nullable=False)
    schedule_times = Column(JSON().with_variant(ARRAY(Time), "postgresql"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    instructions = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    patient = relationship("PatientModel", backref="medications")

    def __repr__(self) -> str:
        return f"<Medication(id={self.id}, name={self.name}, patient_id={self.patient_id})>"
