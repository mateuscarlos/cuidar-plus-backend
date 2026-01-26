"""Inventory Item Domain Service - Business Rules."""
from datetime import datetime
from typing import List, Optional, Tuple

from ..entities.inventory_item import InventoryItem, ItemStatus


class InventoryDomainService:
    """
    Domain Service for Inventory business rules.
    
    Encapsulates business logic for inventory management.
    """
    
    @staticmethod
    def is_low_stock(item: InventoryItem) -> bool:
        """Check if item is low on stock."""
        return item.quantity <= item.min_quantity and item.quantity > 0
    
    @staticmethod
    def is_out_of_stock(item: InventoryItem) -> bool:
        """Check if item is out of stock."""
        return item.quantity == 0
    
    @staticmethod
    def is_expired(item: InventoryItem) -> bool:
        """Check if item is expired."""
        if not item.expiration_date:
            return False
        return item.expiration_date < datetime.utcnow()
    
    @staticmethod
    def calculate_status(item: InventoryItem) -> ItemStatus:
        """
        Calculate automatic status based on item conditions.
        
        Args:
            item: Inventory item
            
        Returns:
            Calculated status
        """
        if InventoryDomainService.is_expired(item):
            return ItemStatus.EXPIRED
        if InventoryDomainService.is_out_of_stock(item):
            return ItemStatus.OUT_OF_STOCK
        if InventoryDomainService.is_low_stock(item):
            return ItemStatus.LOW_STOCK
        return ItemStatus.AVAILABLE
    
    @staticmethod
    def can_perform_output(item: InventoryItem, quantity: int) -> Tuple[bool, str]:
        """
        Check if output operation can be performed.
        
        Args:
            item: Inventory item
            quantity: Quantity to remove
            
        Returns:
            Tuple of (can_perform, reason)
        """
        if InventoryDomainService.is_expired(item):
            return False, "Item está vencido"
        
        if item.quantity < quantity:
            return False, f"Quantidade insuficiente em estoque (disponível: {item.quantity})"
        
        return True, ""
    
    @staticmethod
    def calculate_total_value(item: InventoryItem) -> float:
        """Calculate total value of item in stock."""
        return item.quantity * item.cost_price
    
    @staticmethod
    def validate_for_creation(
        name: str,
        quantity: int,
        min_quantity: int,
        max_quantity: int,
        cost_price: float,
        sale_price: Optional[float] = None,
    ) -> List[str]:
        """
        Validate inventory item data before creation.
        
        Returns:
            List of validation errors
        """
        errors = []
        
        # Validate name
        if not name or len(name.strip()) < 2:
            errors.append("Nome deve ter pelo menos 2 caracteres")
        
        # Validate quantities
        if quantity < 0:
            errors.append("Quantidade não pode ser negativa")
        
        if min_quantity < 0:
            errors.append("Quantidade mínima não pode ser negativa")
        
        if max_quantity < min_quantity:
            errors.append("Quantidade máxima deve ser maior que a mínima")
        
        # Validate prices
        if cost_price < 0:
            errors.append("Preço de custo não pode ser negativo")
        
        if sale_price is not None and sale_price < 0:
            errors.append("Preço de venda não pode ser negativo")
        
        if sale_price is not None and sale_price < cost_price:
            errors.append("Preço de venda não pode ser menor que o custo")
        
        return errors
    
    @staticmethod
    def calculate_reorder_quantity(item: InventoryItem) -> int:
        """
        Calculate recommended reorder quantity.
        
        Args:
            item: Inventory item
            
        Returns:
            Recommended quantity to reorder
        """
        if item.quantity >= item.min_quantity:
            return 0
        
        # Order up to max quantity
        return item.max_quantity - item.quantity
    
    @staticmethod
    def is_near_expiration(item: InventoryItem, days: int = 30) -> bool:
        """
        Check if item is near expiration.
        
        Args:
            item: Inventory item
            days: Number of days threshold
            
        Returns:
            True if expiring within days
        """
        if not item.expiration_date:
            return False
        
        days_until_expiration = (item.expiration_date - datetime.utcnow()).days
        return 0 < days_until_expiration <= days
