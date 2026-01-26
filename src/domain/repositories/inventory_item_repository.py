"""Inventory Item Repository Interface."""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ..entities.inventory_item import InventoryItem, ItemCategory, ItemStatus


class InventoryItemRepository(ABC):
    """Inventory Item Repository Interface."""
    
    @abstractmethod
    async def create(self, item: InventoryItem) -> InventoryItem:
        """Create a new inventory item."""
        pass
    
    @abstractmethod
    async def get_by_id(self, item_id: UUID) -> Optional[InventoryItem]:
        """Get inventory item by ID."""
        pass
    
    @abstractmethod
    async def get_by_code(self, code: str) -> Optional[InventoryItem]:
        """Get inventory item by code."""
        pass
    
    @abstractmethod
    async def get_by_barcode(self, barcode: str) -> Optional[InventoryItem]:
        """Get inventory item by barcode."""
        pass
    
    @abstractmethod
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
        """
        List inventory items with filters.
        
        Returns:
            Tuple of (list of items, total count)
        """
        pass
    
    @abstractmethod
    async def update(self, item: InventoryItem) -> InventoryItem:
        """Update an inventory item."""
        pass
    
    @abstractmethod
    async def delete(self, item_id: UUID) -> bool:
        """Delete an inventory item."""
        pass
    
    @abstractmethod
    async def get_low_stock_items(self, limit: int = 100) -> list[InventoryItem]:
        """Get items with low stock."""
        pass
    
    @abstractmethod
    async def get_expired_items(self, limit: int = 100) -> list[InventoryItem]:
        """Get expired items."""
        pass
