"""Insurer Repository Interface."""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ..entities.insurer import Insurer, InsurerStatus, InsurerType


class InsurerRepository(ABC):
    """Insurer Repository Interface."""
    
    @abstractmethod
    async def create(self, insurer: Insurer) -> Insurer:
        """Create a new insurer."""
        pass
    
    @abstractmethod
    async def get_by_id(self, insurer_id: UUID) -> Optional[Insurer]:
        """Get insurer by ID."""
        pass
    
    @abstractmethod
    async def get_by_cnpj(self, cnpj: str) -> Optional[Insurer]:
        """Get insurer by CNPJ."""
        pass
    
    @abstractmethod
    async def get_by_registration_number(self, registration_number: str) -> Optional[Insurer]:
        """Get insurer by ANS registration number."""
        pass
    
    @abstractmethod
    async def list(
        self,
        search: Optional[str] = None,
        type: Optional[InsurerType] = None,
        status: Optional[InsurerStatus] = None,
        has_active_plans: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Insurer], int]:
        """
        List insurers with filters.
        
        Returns:
            Tuple of (list of insurers, total count)
        """
        pass
    
    @abstractmethod
    async def update(self, insurer: Insurer) -> Insurer:
        """Update an insurer."""
        pass
    
    @abstractmethod
    async def delete(self, insurer_id: UUID) -> bool:
        """Delete an insurer."""
        pass
