"""Report Domain Service - Business Rules."""
from datetime import datetime, timedelta
from typing import List

from ..entities.report import Report, ReportPeriod, ReportType


class ReportDomainService:
    """
    Domain Service for Report business rules.
    
    Encapsulates business logic for report generation and validation.
    """
    
    @staticmethod
    def validate_for_creation(
        title: str,
        start_date: datetime,
        end_date: datetime,
    ) -> List[str]:
        """
        Validate report data before creation.
        
        Returns:
            List of validation errors
        """
        errors = []
        
        # Validate title
        if not title or not title.strip():
            errors.append("Título obrigatório")
        
        # Validate date range
        if start_date > end_date:
            errors.append("Data inicial deve ser anterior à data final")
        
        if end_date > datetime.utcnow():
            errors.append("Data final não pode ser no futuro")
        
        # Validate reasonable date range (max 5 years)
        max_range = timedelta(days=365 * 5)
        if (end_date - start_date) > max_range:
            errors.append("Período muito longo - máximo de 5 anos")
        
        return errors
    
    @staticmethod
    def is_valid_date_range(start_date: datetime, end_date: datetime) -> bool:
        """Check if date range is valid."""
        return start_date <= end_date and end_date <= datetime.utcnow()
    
    @staticmethod
    def get_default_date_range(period: ReportPeriod) -> tuple[datetime, datetime]:
        """
        Get default date range for a period.
        
        Args:
            period: Report period
            
        Returns:
            Tuple of (start_date, end_date)
        """
        end_date = datetime.utcnow()
        
        if period == ReportPeriod.DAILY:
            start_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == ReportPeriod.WEEKLY:
            start_date = end_date - timedelta(days=7)
        elif period == ReportPeriod.MONTHLY:
            start_date = end_date - timedelta(days=30)
        elif period == ReportPeriod.YEARLY:
            start_date = end_date - timedelta(days=365)
        else:  # CUSTOM
            start_date = end_date - timedelta(days=30)
        
        return start_date, end_date
    
    @staticmethod
    def get_report_type_label(report_type: ReportType) -> str:
        """Get human-readable label for report type."""
        labels = {
            ReportType.PATIENTS: "Relatório de Pacientes",
            ReportType.INVENTORY: "Relatório de Estoque",
            ReportType.FINANCIAL: "Relatório Financeiro",
            ReportType.APPOINTMENTS: "Relatório de Atendimentos",
        }
        return labels.get(report_type, report_type.value)
    
    @staticmethod
    def get_report_period_label(period: ReportPeriod) -> str:
        """Get human-readable label for report period."""
        labels = {
            ReportPeriod.DAILY: "Diário",
            ReportPeriod.WEEKLY: "Semanal",
            ReportPeriod.MONTHLY: "Mensal",
            ReportPeriod.YEARLY: "Anual",
            ReportPeriod.CUSTOM: "Personalizado",
        }
        return labels.get(period, period.value)
    
    @staticmethod
    def can_regenerate(report: Report) -> tuple[bool, str]:
        """
        Check if report can be regenerated.
        
        Returns:
            Tuple of (can_regenerate, reason)
        """
        from ..entities.report import ReportStatus
        
        if report.status == ReportStatus.PROCESSING:
            return False, "Relatório está sendo processado"
        
        return True, ""
    
    @staticmethod
    def estimate_generation_time(
        report_type: ReportType,
        start_date: datetime,
        end_date: datetime,
    ) -> int:
        """
        Estimate report generation time in seconds.
        
        Args:
            report_type: Type of report
            start_date: Start date
            end_date: End date
            
        Returns:
            Estimated time in seconds
        """
        # Calculate days in range
        days = (end_date - start_date).days
        
        # Base time by report type (seconds)
        base_times = {
            ReportType.PATIENTS: 5,
            ReportType.INVENTORY: 3,
            ReportType.FINANCIAL: 10,
            ReportType.APPOINTMENTS: 7,
        }
        
        base_time = base_times.get(report_type, 5)
        
        # Add time based on data volume (1 second per 30 days)
        volume_time = days // 30
        
        return base_time + volume_time
