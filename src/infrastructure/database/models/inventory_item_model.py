"""Inventory Item SQLAlchemy Model."""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID

from ..session import Base


class InventoryItemModel(Base):
    """SQLAlchemy model for InventoryItem entity."""
    
    __tablename__ = "inventory_items"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    barcode = Column(String(100), unique=True, nullable=True, index=True)
    category = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    
    # Stock
    quantity = Column(Integer, nullable=False, default=0)
    min_quantity = Column(Integer, nullable=False)
    max_quantity = Column(Integer, nullable=False)
    unit = Column(String(20), nullable=False)
    
    # Status and Control
    status = Column(String(50), nullable=False, default="AVAILABLE")
    location = Column(String(255), nullable=False)
    batch = Column(String(100), nullable=True)
    expiration_date = Column(DateTime, nullable=True)
    
    # Supplier and Prices
    supplier = Column(String(255), nullable=True)
    cost_price = Column(Float, nullable=False)
    sale_price = Column(Float, nullable=True)
    
    # Observations
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        return f"<InventoryItem(id={self.id}, name={self.name}, code={self.code})>"


class StockMovementModel(Base):
    """SQLAlchemy model for StockMovement entity."""
    
    __tablename__ = "stock_movements"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    item_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    type = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False)
    reason = Column(Text, nullable=False)
    performed_by = Column(String(255), nullable=False)
    previous_quantity = Column(Integer, nullable=False)
    new_quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        return f"<StockMovement(id={self.id}, item_id={self.item_id}, type={self.type})>"
