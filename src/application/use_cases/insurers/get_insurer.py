"""Get Insurer Use Case."""
from uuid import UUID

from src.domain.entities.insurer import Insurer
from src.domain.repositories.insurer_repository import InsurerRepository
from src.shared.exceptions.application_exception import ApplicationException


class GetInsurerUseCase:
    """Use Case: Get a single insurer by ID."""
    
    def __init__(self, insurer_repository: InsurerRepository) -> None:
        self._insurer_repository = insurer_repository
    
    async def execute(self, insurer_id: UUID) -> Insurer:
        """Execute the use case."""
        
        insurer = await self._insurer_repository.get_by_id(insurer_id)
        
        if not insurer:
            raise ApplicationException(
                message="Operadora não encontrada",
                code="INSURER_NOT_FOUND",
            )
        
        return insurer
