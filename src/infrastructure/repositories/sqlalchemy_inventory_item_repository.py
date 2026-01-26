"""SQLAlchemy Inventory Item Repository Implementation."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.domain.entities.inventory_item import (
    InventoryItem,
    ItemCategory,
    ItemStatus,
    MeasurementUnit,
)
from src.domain.repositories.inventory_item_repository import InventoryItemRepository
from src.infrastructure.database.models.inventory_item_model import InventoryItemModel


class SQLAlchemyInventoryItemRepository(InventoryItemRepository):
    """SQLAlchemy implementation of InventoryItemRepository."""
    
    def __init__(self, session: Session) -> None:
        self._session = session
    
    async def create(self, item: InventoryItem) -> InventoryItem:
        """Create a new inventory item."""
        item_model = self._to_model(item)
        self._session.add(item_model)
        self._session.flush()
        return self._to_entity(item_model)
    
    async def get_by_id(self, item_id: UUID) -> Optional[InventoryItem]:
        """Get inventory item by ID."""
        item_model = self._session.query(InventoryItemModel).filter(
            InventoryItemModel.id == item_id
        ).first()
        
        return self._to_entity(item_model) if item_model else None
    
    async def get_by_code(self, code: str) -> Optional[InventoryItem]:
        """Get inventory item by code."""
        item_model = self._session.query(InventoryItemModel).filter(
            InventoryItemModel.code == code
        ).first()
        
        return self._to_entity(item_model) if item_model else None
    
    async def get_by_barcode(self, barcode: str) -> Optional[InventoryItem]:
        """Get inventory item by barcode."""
        item_model = self._session.query(InventoryItemModel).filter(
            InventoryItemModel.barcode == barcode
        ).first()
        
        return self._to_entity(item_model) if item_model else None
    
    async def list(
        self,
        search: Optional[str] = None,
        category: Optional[ItemCategory] = None,
        status: Optional[ItemStatus] = None,
        low_stock: Optional[bool] = None,
        expired: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[InventoryItem], int]:
        """List inventory items with filters."""
        query = self._session.query(InventoryItemModel)
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    InventoryItemModel.name.ilike(search_filter),
                    InventoryItemModel.code.like(search_filter),
                    InventoryItemModel.barcode.like(search_filter),
                )
            )
        
        if category:
            query = query.filter(InventoryItemModel.category == category.value)
        
        if status:
            query = query.filter(InventoryItemModel.status == status.value)
        
        if low_stock:
            query = query.filter(
                InventoryItemModel.quantity <= InventoryItemModel.min_quantity
            )
        
        if expired:
            query = query.filter(
                InventoryItemModel.expiration_date < datetime.utcnow()
            )
        
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        
        return [self._to_entity(model) for model in items], total
    
    async def update(self, item: InventoryItem) -> InventoryItem:
        """Update an inventory item."""
        item_model = self._to_model(item)
        self._session.merge(item_model)
        self._session.flush()
        return self._to_entity(item_model)
    
    async def delete(self, item_id: UUID) -> bool:
        """Delete an inventory item."""
        result = self._session.query(InventoryItemModel).filter(
            InventoryItemModel.id == item_id
        ).delete()
        self._session.flush()
        return result > 0
    
    async def get_low_stock_items(self, limit: int = 100) -> list[InventoryItem]:
        """Get items with low stock."""
        items = self._session.query(InventoryItemModel).filter(
            InventoryItemModel.quantity <= InventoryItemModel.min_quantity
        ).limit(limit).all()
        
        return [self._to_entity(model) for model in items]
    
    async def get_expired_items(self, limit: int = 100) -> list[InventoryItem]:
        """Get expired items."""
        items = self._session.query(InventoryItemModel).filter(
            InventoryItemModel.expiration_date < datetime.utcnow()
        ).limit(limit).all()
        
        return [self._to_entity(model) for model in items]
    
    @staticmethod
    def _to_model(item: InventoryItem) -> InventoryItemModel:
        """Convert domain entity to database model."""
        return InventoryItemModel(
            id=item.id,
            name=item.name,
            code=item.code,
            barcode=item.barcode,
            category=item.category.value,
            description=item.description,
            quantity=item.quantity,
            min_quantity=item.min_quantity,
            max_quantity=item.max_quantity,
            unit=item.unit.value,
            status=item.status.value,
            location=item.location,
            batch=item.batch,
            expiration_date=item.expiration_date,
            supplier=item.supplier,
            cost_price=item.cost_price,
            sale_price=item.sale_price,
            notes=item.notes,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )
    
    @staticmethod
    def _to_entity(model: InventoryItemModel) -> InventoryItem:
        """Convert database model to domain entity."""
        return InventoryItem(
            id=model.id,
            name=model.name,
            code=model.code,
            barcode=model.barcode,
            category=ItemCategory(model.category),
            description=model.description,
            quantity=model.quantity,
            min_quantity=model.min_quantity,
            max_quantity=model.max_quantity,
            unit=MeasurementUnit(model.unit),
            status=ItemStatus(model.status),
            location=model.location,
            batch=model.batch,
            expiration_date=model.expiration_date,
            supplier=model.supplier,
            cost_price=model.cost_price,
            sale_price=model.sale_price,
            notes=model.notes,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
