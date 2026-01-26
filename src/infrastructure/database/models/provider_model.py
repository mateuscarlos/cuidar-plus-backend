"""Provider SQLAlchemy Model."""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSON, UUID

from ..session import Base


class ProviderModel(Base):
    """SQLAlchemy model for Provider entity."""
    
    __tablename__ = "providers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False, index=True)
    trade_name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default="PENDING_APPROVAL")
    
    # Identification
    document = Column(String(20), unique=True, nullable=False, index=True)
    credentials = Column(JSON, nullable=False)  # List of credentials
    
    # Specialties - stored as JSON array
    specialties = Column(JSON, nullable=False)
    
    # Contact Data
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    website = Column(String(255), nullable=True)
    
    # Address - stored as JSON
    address = Column(JSON, nullable=False)
    
    # Working Hours - stored as JSON
    working_hours = Column(JSON, nullable=True)
    
    # Services - stored as JSON array
    services = Column(JSON, nullable=True, default=[])
    
    # Accepted Insurers - stored as JSON array of UUIDs
    accepted_insurers = Column(JSON, nullable=True, default=[])
    
    # Additional Info
    logo = Column(Text, nullable=True)
    capacity = Column(Integer, nullable=True)
    has_emergency = Column(Boolean, default=False, nullable=False)
    rating = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        return f"<Provider(id={self.id}, name={self.name}, document={self.document})>"
