"""Update Insurer Use Case."""
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.domain.entities.insurer import InsurerStatus
from src.domain.repositories.insurer_repository import InsurerRepository
from src.domain.services.insurer_service import InsurerDomainService
from src.shared.exceptions.application_exception import ApplicationException


@dataclass
class UpdateInsurerInput:
    """Input DTO for UpdateInsurer use case."""
    
    id: UUID
    name: Optional[str] = None
    trade_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    status: Optional[str] = None
    logo: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class UpdateInsurerOutput:
    """Output DTO for UpdateInsurer use case."""
    
    id: UUID
    name: str
    status: str


class UpdateInsurerUseCase:
    """
    Use Case: Update an existing insurer.
    
    Business Rules:
    - Validate all fields being updated
    - Check if insurer can be deactivated (no active plans)
    - Validate email format
    """
    
    def __init__(self, insurer_repository: InsurerRepository) -> None:
        self._insurer_repository = insurer_repository
    
    async def execute(self, input_dto: UpdateInsurerInput) -> UpdateInsurerOutput:
        """Execute the use case."""
        
        # Get existing insurer
        insurer = await self._insurer_repository.get_by_id(input_dto.id)
        if not insurer:
            raise ApplicationException(
                message="Operadora não encontrada",
                code="INSURER_NOT_FOUND",
            )
        
        # Check if trying to deactivate using Domain Service
        if input_dto.status and input_dto.status != insurer.status.value:
            new_status = InsurerStatus(input_dto.status)
            if new_status == InsurerStatus.INACTIVE:
                can_deactivate, reason = InsurerDomainService.can_be_deactivated(insurer)
                if not can_deactivate:
                    raise ApplicationException(
                        message=reason,
                        code="CANNOT_DEACTIVATE",
                    )
        
        insurer.update(
            name=input_dto.name,
            trade_name=input_dto.trade_name,
            phone=input_dto.phone,
            email=input_dto.email,
            website=input_dto.website,
            logo=input_dto.logo,
            notes=input_dto.notes,
        )
        
        insurer = await self._insurer_repository.update(insurer)
        
        return UpdateInsurerOutput(
            id=insurer.id,
            name=insurer.name,
            status=insurer.status.value,
        )
