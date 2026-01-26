"""Provider Repository Interface."""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ..entities.provider import Provider, ProviderSpecialty, ProviderStatus, ProviderType


class ProviderRepository(ABC):
    """Provider Repository Interface."""
    
    @abstractmethod
    async def create(self, provider: Provider) -> Provider:
        """Create a new provider."""
        pass
    
    @abstractmethod
    async def get_by_id(self, provider_id: UUID) -> Optional[Provider]:
        """Get provider by ID."""
        pass
    
    @abstractmethod
    async def get_by_document(self, document: str) -> Optional[Provider]:
        """Get provider by document (CNPJ or CPF)."""
        pass
    
    @abstractmethod
    async def list(
        self,
        search: Optional[str] = None,
        type: Optional[ProviderType] = None,
        status: Optional[ProviderStatus] = None,
        specialty: Optional[ProviderSpecialty] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        accepts_insurer: Optional[UUID] = None,
        has_emergency: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Provider], int]:
        """
        List providers with filters.
        
        Returns:
            Tuple of (list of providers, total count)
        """
        pass
    
    @abstractmethod
    async def update(self, provider: Provider) -> Provider:
        """Update a provider."""
        pass
    
    @abstractmethod
    async def delete(self, provider_id: UUID) -> bool:
        """Delete a provider."""
        pass
    
    @abstractmethod
    async def get_pending_approval(self, limit: int = 100) -> list[Provider]:
        """Get providers pending approval."""
        pass
