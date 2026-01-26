"""Report SQLAlchemy Model."""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import relationship

from ..session import Base


class ReportModel(Base):
    """SQLAlchemy model for Report entity."""
    
    __tablename__ = "reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    type = Column(String(50), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    period = Column(String(50), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    format = Column(String(20), nullable=False)
    generated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status = Column(String(50), nullable=False, default="PENDING", index=True)
    download_url = Column(Text, nullable=True)
    data = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    generator = relationship("UserModel", backref="reports")
    
    def __repr__(self) -> str:
        return f"<Report(id={self.id}, type={self.type}, status={self.status})>"
