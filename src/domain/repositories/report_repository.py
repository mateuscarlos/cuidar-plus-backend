"""Report Repository Interface."""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ..entities.report import Report, ReportStatus, ReportType


class ReportRepository(ABC):
    """Report Repository Interface."""
    
    @abstractmethod
    async def create(self, report: Report) -> Report:
        """Create a new report."""
        pass
    
    @abstractmethod
    async def get_by_id(self, report_id: UUID) -> Optional[Report]:
        """Get report by ID."""
        pass
    
    @abstractmethod
    async def list(
        self,
        type: Optional[ReportType] = None,
        status: Optional[ReportStatus] = None,
        generated_by: Optional[UUID] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Report], int]:
        """
        List reports with filters.
        
        Returns:
            Tuple of (list of reports, total count)
        """
        pass
    
    @abstractmethod
    async def update(self, report: Report) -> Report:
        """Update a report."""
        pass
    
    @abstractmethod
    async def delete(self, report_id: UUID) -> bool:
        """Delete a report."""
        pass
    
    @abstractmethod
    async def get_pending_reports(self, limit: int = 100) -> list[Report]:
        """Get pending reports."""
        pass
