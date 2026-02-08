"""Patient SQLAlchemy Model."""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..session import Base


class PatientModel(Base):
    """SQLAlchemy model for Patient entity."""
    
    __tablename__ = "patients"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # Bolt: Added index=True to improve performance of queries filtering by caregiver
    caregiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False, index=True)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    address = Column(Text, nullable=False)
    phone = Column(String(20), nullable=False)
    emergency_contact = Column(String(255), nullable=False)
    emergency_phone = Column(String(20), nullable=False)
    medical_conditions = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    observations = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    caregiver = relationship("UserModel", backref="patients")
    
    def __repr__(self) -> str:
        return f"<Patient(id={self.id}, name={self.full_name}, cpf={self.cpf})>"
