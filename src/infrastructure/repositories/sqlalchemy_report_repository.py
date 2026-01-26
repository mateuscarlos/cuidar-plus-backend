"""SQLAlchemy Report Repository Implementation."""
from typing import Any, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.domain.entities.report import Report, ReportStatus, ReportType
from src.domain.repositories.report_repository import ReportRepository
from src.infrastructure.database.models.report_model import ReportModel


class SQLAlchemyReportRepository(ReportRepository):
    """SQLAlchemy implementation of ReportRepository."""
    
    def __init__(self, session: Session) -> None:
        self._session = session
    
    async def create(self, report: Report) -> Report:
        """Create a new report."""
        report_model = self._to_model(report)
        self._session.add(report_model)
        self._session.flush()
        return self._to_entity(report_model)
    
    async def get_by_id(self, report_id: UUID) -> Optional[Report]:
        """Get report by ID."""
        report_model = self._session.query(ReportModel).filter(
            ReportModel.id == report_id
        ).first()
        
        return self._to_entity(report_model) if report_model else None
    
    async def list(
        self,
        type: Optional[ReportType] = None,
        status: Optional[ReportStatus] = None,
        generated_by: Optional[UUID] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Report], int]:
        """List reports with filters."""
        query = self._session.query(ReportModel)
        
        if type:
            query = query.filter(ReportModel.type == type.value)
        
        if status:
            query = query.filter(ReportModel.status == status.value)
        
        if generated_by:
            query = query.filter(ReportModel.generated_by == generated_by)
        
        total = query.count()
        reports = query.order_by(ReportModel.created_at.desc()).offset(skip).limit(limit).all()
        
        return [self._to_entity(model) for model in reports], total
    
    async def update(self, report: Report) -> Report:
        """Update a report."""
        report_model = self._to_model(report)
        self._session.merge(report_model)
        self._session.flush()
        return self._to_entity(report_model)
    
    async def delete(self, report_id: UUID) -> bool:
        """Delete a report."""
        result = self._session.query(ReportModel).filter(
            ReportModel.id == report_id
        ).delete()
        self._session.flush()
        return result > 0
    
    async def get_pending_reports(self, limit: int = 100) -> list[Report]:
        """Get pending reports."""
        reports = self._session.query(ReportModel).filter(
            ReportModel.status == ReportStatus.PENDING.value
        ).limit(limit).all()
        
        return [self._to_entity(model) for model in reports]
    
    @staticmethod
    def _to_model(report: Report) -> ReportModel:
        """Convert domain entity to database model."""
        return ReportModel(
            id=report.id,
            type=report.type.value,
            title=report.title,
            period=report.period.value,
            start_date=report.start_date,
            end_date=report.end_date,
            format=report.format.value,
            generated_by=report.generated_by,
            status=report.status.value,
            download_url=report.download_url,
            data=report.data,
            error_message=report.error_message,
            created_at=report.created_at,
            updated_at=report.updated_at,
            completed_at=report.completed_at,
        )
    
    @staticmethod
    def _to_entity(model: ReportModel) -> Report:
        """Convert database model to domain entity."""
        return Report(
            id=model.id,
            type=ReportType(model.type),
            title=model.title,
            period=model.period,
            start_date=model.start_date,
            end_date=model.end_date,
            format=model.format,
            generated_by=model.generated_by,
            status=ReportStatus(model.status),
            download_url=model.download_url,
            data=model.data,
            error_message=model.error_message,
            created_at=model.created_at,
            updated_at=model.updated_at,
            completed_at=model.completed_at,
        )
