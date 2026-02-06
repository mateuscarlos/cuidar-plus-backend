"""Appointment SQLAlchemy Model."""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..session import Base


class AppointmentModel(Base):
    """SQLAlchemy model for Appointment entity."""
    
    __tablename__ = "appointments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    appointment_date = Column(DateTime, nullable=False, index=True)
    duration_minutes = Column(Integer, nullable=False)
    location = Column(String(500), nullable=False)
    doctor_name = Column(String(255), nullable=True)
    specialty = Column(String(100), nullable=True)
    status = Column(String(50), default="scheduled", nullable=False, index=True)
    reminder_sent = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    patient = relationship("PatientModel", backref="appointments")
    
    def __repr__(self) -> str:
        return f"<Appointment(id={self.id}, title={self.title}, date={self.appointment_date})>"
