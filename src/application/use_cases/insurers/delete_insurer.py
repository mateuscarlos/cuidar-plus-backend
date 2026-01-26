"""Delete Insurer Use Case."""
from uuid import UUID

from src.domain.repositories.insurer_repository import InsurerRepository
from src.domain.services.insurer_service import InsurerDomainService
from src.shared.exceptions.application_exception import ApplicationException


class DeleteInsurerUseCase:
    """
    Use Case: Delete an insurer.
    
    Business Rules:
    - Check if insurer can be deleted (no active plans)
    - Soft delete or hard delete based on business rules
    """
    
    def __init__(self, insurer_repository: InsurerRepository) -> None:
        self._insurer_repository = insurer_repository
    
    async def execute(self, insurer_id: UUID) -> bool:
        """Execute the use case."""
        
        # Get insurer
        insurer = await self._insurer_repository.get_by_id(insurer_id)
        if not insurer:
            raise ApplicationException(
                message="Operadora não encontrada",
                code="INSURER_NOT_FOUND",
            )
        
        # Check if can be deleted
        can_deactivate, reason = InsurerDomainService.can_be_deactivated(insurer)
        if not can_deactivate:
            raise ApplicationException(
                message=f"Não é possível excluir a operadora: {reason}",
                code="CANNOT_DELETE",
            )
        
        # Delete insurer
        success = await self._insurer_repository.delete(insurer_id)
        
        return success
