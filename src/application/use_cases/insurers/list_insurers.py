"""List Insurers Use Case."""
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.domain.entities.insurer import InsurerStatus, InsurerType
from src.domain.repositories.insurer_repository import InsurerRepository


@dataclass
class ListInsurersInput:
    """Input DTO for ListInsurers use case."""
    
    search: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    has_active_plans: Optional[bool] = None
    page: int = 1
    page_size: int = 50


@dataclass
class InsurerItem:
    """Individual insurer item."""
    
    id: UUID
    name: str
    trade_name: str
    cnpj: str
    type: str
    status: str
    phone: str
    email: str


@dataclass
class ListInsurersOutput:
    """Output DTO for ListInsurers use case."""
    
    items: list[InsurerItem]
    total: int
    page: int
    page_size: int


class ListInsurersUseCase:
    """Use Case: List insurers with filters."""
    
    def __init__(self, insurer_repository: InsurerRepository) -> None:
        self._insurer_repository = insurer_repository
    
    async def execute(self, input_dto: ListInsurersInput) -> ListInsurersOutput:
        """Execute the use case."""
        
        skip = (input_dto.page - 1) * input_dto.page_size
        
        insurers, total = await self._insurer_repository.list(
            search=input_dto.search,
            type=InsurerType(input_dto.type) if input_dto.type else None,
            status=InsurerStatus(input_dto.status) if input_dto.status else None,
            has_active_plans=input_dto.has_active_plans,
            skip=skip,
            limit=input_dto.page_size,
        )
        
        items = [
            InsurerItem(
                id=insurer.id,
                name=insurer.name,
                trade_name=insurer.trade_name,
                cnpj=insurer.cnpj,
                type=insurer.type.value,
                status=insurer.status.value,
                phone=insurer.phone,
                email=insurer.email,
            )
            for insurer in insurers
        ]
        
        return ListInsurersOutput(
            items=items,
            total=total,
            page=input_dto.page,
            page_size=input_dto.page_size,
        )
