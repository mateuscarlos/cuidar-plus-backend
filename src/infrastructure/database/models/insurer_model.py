"""Insurer SQLAlchemy Model."""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, Float, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSON, UUID
from sqlalchemy.orm import relationship

from ..session import Base


class InsurerModel(Base):
    """SQLAlchemy model for Insurer entity."""
    
    __tablename__ = "insurers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    trade_name = Column(String(255), nullable=False)
    cnpj = Column(String(14), unique=True, nullable=False, index=True)
    registration_number = Column(String(50), unique=True, nullable=False, index=True)
    type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default="ACTIVE")
    
    # Contact Data
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    website = Column(String(255), nullable=True)
    
    # Address - stored as JSON
    address = Column(JSON, nullable=False)
    
    # Plans - stored as JSON array
    plans = Column(JSON, nullable=True, default=[])
    
    # Additional Info
    logo = Column(Text, nullable=True)
    contract_start_date = Column(DateTime, nullable=True)
    contract_end_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        return f"<Insurer(id={self.id}, name={self.name}, cnpj={self.cnpj})>"
