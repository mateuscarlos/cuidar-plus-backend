"""Inventory Item Entity."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class ItemCategory(str, Enum):
    """Item Category."""
    
    MEDICATION = "MEDICATION"
    EQUIPMENT = "EQUIPMENT"
    SUPPLIES = "SUPPLIES"
    CONSUMABLES = "CONSUMABLES"


class ItemStatus(str, Enum):
    """Item Status."""
    
    AVAILABLE = "AVAILABLE"
    LOW_STOCK = "LOW_STOCK"
    OUT_OF_STOCK = "OUT_OF_STOCK"
    EXPIRED = "EXPIRED"
    RESERVED = "RESERVED"


class MeasurementUnit(str, Enum):
    """Measurement Unit."""
    
    UNIT = "UNIT"
    BOX = "BOX"
    BOTTLE = "BOTTLE"
    TUBE = "TUBE"
    SACHET = "SACHET"
    ML = "ML"
    MG = "MG"
    G = "G"
    KG = "KG"


class MovementType(str, Enum):
    """Stock Movement Type."""
    
    IN = "IN"  # Entrada
    OUT = "OUT"  # Saída
    ADJUSTMENT = "ADJUSTMENT"  # Ajuste
    TRANSFER = "TRANSFER"  # Transferência


@dataclass
class StockMovement:
    """Stock Movement."""
    
    id: UUID
    item_id: UUID
    type: MovementType
    quantity: int
    reason: str
    performed_by: str
    previous_quantity: int
    new_quantity: int
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class InventoryItem:
    """
    Inventory Item Entity.
    
    Represents an item in the inventory/stock.
    """
    
    id: UUID
    name: str
    code: str
    category: ItemCategory
    quantity: int
    min_quantity: int
    max_quantity: int
    unit: MeasurementUnit
    status: ItemStatus
    location: str
    cost_price: float
    barcode: Optional[str] = None
    description: Optional[str] = None
    batch: Optional[str] = None
    expiration_date: Optional[datetime] = None
    supplier: Optional[str] = None
    sale_price: Optional[float] = None
    notes: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    @classmethod
    def create(
        cls,
        name: str,
        category: ItemCategory,
        quantity: int,
        min_quantity: int,
        max_quantity: int,
        unit: MeasurementUnit,
        location: str,
        cost_price: float,
        barcode: Optional[str] = None,
        description: Optional[str] = None,
        batch: Optional[str] = None,
        expiration_date: Optional[datetime] = None,
        supplier: Optional[str] = None,
        sale_price: Optional[float] = None,
        notes: Optional[str] = None,
    ) -> "InventoryItem":
        """
        Create a new Inventory Item.
        
        Args:
            name: Item name
            category: Item category
            quantity: Current quantity
            min_quantity: Minimum quantity threshold
            max_quantity: Maximum quantity threshold
            unit: Measurement unit
            location: Storage location
            cost_price: Cost price
            barcode: Item barcode
            description: Item description
            batch: Batch number
            expiration_date: Expiration date
            supplier: Supplier name
            sale_price: Sale price
            notes: Additional notes
            
        Returns:
            New InventoryItem instance
        """
        cls._validate_quantities(quantity, min_quantity, max_quantity)
        cls._validate_prices(cost_price, sale_price)
        
        item_id = uuid4()
        code = cls._generate_code(item_id)
        status = cls._calculate_status(quantity, min_quantity, expiration_date)
        
        return cls(
            id=item_id,
            name=name,
            code=code,
            category=category,
            quantity=quantity,
            min_quantity=min_quantity,
            max_quantity=max_quantity,
            unit=unit,
            status=status,
            location=location,
            cost_price=cost_price,
            barcode=barcode,
            description=description,
            batch=batch,
            expiration_date=expiration_date,
            supplier=supplier,
            sale_price=sale_price,
            notes=notes,
        )
    
    def update(
        self,
        name: Optional[str] = None,
        category: Optional[ItemCategory] = None,
        min_quantity: Optional[int] = None,
        max_quantity: Optional[int] = None,
        unit: Optional[MeasurementUnit] = None,
        location: Optional[str] = None,
        cost_price: Optional[float] = None,
        barcode: Optional[str] = None,
        description: Optional[str] = None,
        batch: Optional[str] = None,
        expiration_date: Optional[datetime] = None,
        supplier: Optional[str] = None,
        sale_price: Optional[float] = None,
        notes: Optional[str] = None,
    ) -> None:
        """Update item information."""
        if name is not None:
            self.name = name
        if category is not None:
            self.category = category
        if min_quantity is not None:
            self.min_quantity = min_quantity
        if max_quantity is not None:
            self.max_quantity = max_quantity
        if unit is not None:
            self.unit = unit
        if location is not None:
            self.location = location
        if cost_price is not None:
            self._validate_prices(cost_price, sale_price or self.sale_price)
            self.cost_price = cost_price
        if barcode is not None:
            self.barcode = barcode
        if description is not None:
            self.description = description
        if batch is not None:
            self.batch = batch
        if expiration_date is not None:
            self.expiration_date = expiration_date
        if supplier is not None:
            self.supplier = supplier
        if sale_price is not None:
            self._validate_prices(self.cost_price, sale_price)
            self.sale_price = sale_price
        if notes is not None:
            self.notes = notes
        
        self._update_status()
        self.updated_at = datetime.utcnow()
    
    def adjust_quantity(self, new_quantity: int, reason: str, performed_by: str) -> StockMovement:
        """Adjust item quantity."""
        previous_quantity = self.quantity
        self.quantity = new_quantity
        self._update_status()
        self.updated_at = datetime.utcnow()
        
        movement_type = MovementType.IN if new_quantity > previous_quantity else MovementType.OUT
        quantity_diff = abs(new_quantity - previous_quantity)
        
        return StockMovement(
            id=uuid4(),
            item_id=self.id,
            type=movement_type,
            quantity=quantity_diff,
            reason=reason,
            performed_by=performed_by,
            previous_quantity=previous_quantity,
            new_quantity=new_quantity,
        )
    
    def add_stock(self, quantity: int, reason: str, performed_by: str) -> StockMovement:
        """Add stock quantity."""
        previous_quantity = self.quantity
        self.quantity += quantity
        self._update_status()
        self.updated_at = datetime.utcnow()
        
        return StockMovement(
            id=uuid4(),
            item_id=self.id,
            type=MovementType.IN,
            quantity=quantity,
            reason=reason,
            performed_by=performed_by,
            previous_quantity=previous_quantity,
            new_quantity=self.quantity,
        )
    
    def remove_stock(self, quantity: int, reason: str, performed_by: str) -> StockMovement:
        """Remove stock quantity."""
        if quantity > self.quantity:
            raise ValueError("Quantidade insuficiente em estoque")
        
        previous_quantity = self.quantity
        self.quantity -= quantity
        self._update_status()
        self.updated_at = datetime.utcnow()
        
        return StockMovement(
            id=uuid4(),
            item_id=self.id,
            type=MovementType.OUT,
            quantity=quantity,
            reason=reason,
            performed_by=performed_by,
            previous_quantity=previous_quantity,
            new_quantity=self.quantity,
        )
    
    def _update_status(self) -> None:
        """Update item status based on current conditions."""
        self.status = self._calculate_status(
            self.quantity,
            self.min_quantity,
            self.expiration_date
        )
    
    @staticmethod
    def _calculate_status(
        quantity: int,
        min_quantity: int,
        expiration_date: Optional[datetime]
    ) -> ItemStatus:
        """Calculate item status."""
        if expiration_date and expiration_date < datetime.utcnow():
            return ItemStatus.EXPIRED
        if quantity == 0:
            return ItemStatus.OUT_OF_STOCK
        if quantity <= min_quantity:
            return ItemStatus.LOW_STOCK
        return ItemStatus.AVAILABLE
    
    @staticmethod
    def _generate_code(item_id: UUID) -> str:
        """Generate item code."""
        return f"INV-{str(item_id)[:8].upper()}"
    
    @staticmethod
    def _validate_quantities(quantity: int, min_quantity: int, max_quantity: int) -> None:
        """Validate quantities."""
        if quantity < 0:
            raise ValueError("Quantidade não pode ser negativa")
        if min_quantity < 0:
            raise ValueError("Quantidade mínima não pode ser negativa")
        if max_quantity < min_quantity:
            raise ValueError("Quantidade máxima deve ser maior que a mínima")
    
    @staticmethod
    def _validate_prices(cost_price: float, sale_price: Optional[float]) -> None:
        """Validate prices."""
        if cost_price < 0:
            raise ValueError("Preço de custo não pode ser negativo")
        if sale_price is not None and sale_price < 0:
            raise ValueError("Preço de venda não pode ser negativo")
