"""Report Entity."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID, uuid4


class ReportType(str, Enum):
    """Report Type."""
    
    PATIENTS = "PATIENTS"
    INVENTORY = "INVENTORY"
    FINANCIAL = "FINANCIAL"
    APPOINTMENTS = "APPOINTMENTS"


class ReportPeriod(str, Enum):
    """Report Period."""
    
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"
    CUSTOM = "CUSTOM"


class ReportFormat(str, Enum):
    """Report Format."""
    
    PDF = "PDF"
    EXCEL = "EXCEL"
    CSV = "CSV"


class ReportStatus(str, Enum):
    """Report Status."""
    
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class ReportSummary:
    """Report Summary Data."""
    
    total_patients: int = 0
    new_patients: int = 0
    discharged_patients: int = 0
    active_patients: int = 0
    total_revenue: float = 0.0
    total_expenses: float = 0.0
    inventory_value: float = 0.0
    low_stock_items: int = 0


@dataclass
class Report:
    """
    Report Entity.
    
    Represents a generated report with data and metadata.
    """
    
    id: UUID
    type: ReportType
    title: str
    period: ReportPeriod
    start_date: datetime
    end_date: datetime
    format: ReportFormat
    generated_by: UUID  # User ID
    status: ReportStatus
    download_url: Optional[str] = None
    data: Optional[dict[str, Any]] = None
    error_message: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    @classmethod
    def create(
        cls,
        type: ReportType,
        title: str,
        period: ReportPeriod,
        start_date: datetime,
        end_date: datetime,
        format: ReportFormat,
        generated_by: UUID,
    ) -> "Report":
        """
        Create a new Report.
        
        Args:
            type: Type of report
            title: Report title
            period: Time period
            start_date: Start date
            end_date: End date
            format: Output format
            generated_by: User ID who requested the report
            
        Returns:
            New Report instance
        """
        cls._validate_dates(start_date, end_date)
        
        return cls(
            id=uuid4(),
            type=type,
            title=title,
            period=period,
            start_date=start_date,
            end_date=end_date,
            format=format,
            generated_by=generated_by,
            status=ReportStatus.PENDING,
        )
    
    def start_processing(self) -> None:
        """Mark report as processing."""
        if self.status != ReportStatus.PENDING:
            raise ValueError("Apenas relatórios pendentes podem iniciar processamento")
        self.status = ReportStatus.PROCESSING
        self.updated_at = datetime.utcnow()
    
    def complete(self, download_url: str, data: Optional[dict[str, Any]] = None) -> None:
        """Mark report as completed."""
        if self.status != ReportStatus.PROCESSING:
            raise ValueError("Apenas relatórios em processamento podem ser concluídos")
        self.status = ReportStatus.COMPLETED
        self.download_url = download_url
        self.data = data
        self.completed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def fail(self, error_message: str) -> None:
        """Mark report as failed."""
        if self.status not in [ReportStatus.PENDING, ReportStatus.PROCESSING]:
            raise ValueError("Apenas relatórios pendentes ou em processamento podem falhar")
        self.status = ReportStatus.FAILED
        self.error_message = error_message
        self.updated_at = datetime.utcnow()
    
    def retry(self) -> None:
        """Retry failed report."""
        if self.status != ReportStatus.FAILED:
            raise ValueError("Apenas relatórios falhados podem ser reprocessados")
        self.status = ReportStatus.PENDING
        self.error_message = None
        self.updated_at = datetime.utcnow()
    
    @staticmethod
    def _validate_dates(start_date: datetime, end_date: datetime) -> None:
        """Validate date range."""
        if start_date > end_date:
            raise ValueError("Data inicial deve ser anterior à data final")
        if end_date > datetime.utcnow():
            raise ValueError("Data final não pode ser no futuro")
