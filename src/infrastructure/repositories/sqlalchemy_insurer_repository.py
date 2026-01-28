"""SQLAlchemy Insurer Repository Implementation."""
from typing import Optional
from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.domain.entities.insurer import (
    Insurer,
    InsurerAddress,
    InsurerPlan,
    InsurerStatus,
    InsurerType,
    PlanType,
)
from src.domain.repositories.insurer_repository import InsurerRepository
from src.infrastructure.database.models.insurer_model import InsurerModel


class SQLAlchemyInsurerRepository(InsurerRepository):
    """SQLAlchemy implementation of InsurerRepository."""
    
    def __init__(self, session: Session) -> None:
        self._session = session
    
    async def create(self, insurer: Insurer) -> Insurer:
        """Create a new insurer."""
        insurer_model = self._to_model(insurer)
        self._session.add(insurer_model)
        self._session.flush()
        return self._to_entity(insurer_model)
    
    async def get_by_id(self, insurer_id: UUID) -> Optional[Insurer]:
        """Get insurer by ID."""
        insurer_model = self._session.query(InsurerModel).filter(
            InsurerModel.id == insurer_id
        ).first()
        
        return self._to_entity(insurer_model) if insurer_model else None
    
    async def get_by_cnpj(self, cnpj: str) -> Optional[Insurer]:
        """Get insurer by CNPJ."""
        cnpj_numbers = ''.join(filter(str.isdigit, cnpj))
        insurer_model = self._session.query(InsurerModel).filter(
            InsurerModel.cnpj == cnpj_numbers
        ).first()
        
        return self._to_entity(insurer_model) if insurer_model else None
    
    async def get_by_registration_number(self, registration_number: str) -> Optional[Insurer]:
        """Get insurer by ANS registration number."""
        insurer_model = self._session.query(InsurerModel).filter(
            InsurerModel.registration_number == registration_number
        ).first()
        
        return self._to_entity(insurer_model) if insurer_model else None
    
    async def list(
        self,
        search: Optional[str] = None,
        type: Optional[InsurerType] = None,
        status: Optional[InsurerStatus] = None,
        has_active_plans: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Insurer], int]:
        """List insurers with filters."""
        query = self._session.query(InsurerModel)
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    InsurerModel.name.ilike(search_filter),
                    InsurerModel.trade_name.ilike(search_filter),
                    InsurerModel.cnpj.like(search_filter),
                )
            )
        
        if type:
            query = query.filter(InsurerModel.type == type.value)
        
        if status:
            query = query.filter(InsurerModel.status == status.value)
        
        # TODO: Implement has_active_plans filter with JSON query
        
        total = query.count()
        insurers = query.offset(skip).limit(limit).all()
        
        return [self._to_entity(model) for model in insurers], total
    
    async def update(self, insurer: Insurer) -> Insurer:
        """Update an insurer."""
        insurer_model = self._to_model(insurer)
        self._session.merge(insurer_model)
        self._session.flush()
        return self._to_entity(insurer_model)
    
    async def delete(self, insurer_id: UUID) -> bool:
        """Delete an insurer."""
        result = self._session.query(InsurerModel).filter(
            InsurerModel.id == insurer_id
        ).delete()
        self._session.flush()
        return result > 0
    
    @staticmethod
    def _to_model(insurer: Insurer) -> InsurerModel:
        """Convert domain entity to database model."""
        return InsurerModel(
            id=insurer.id,
            name=insurer.name,
            trade_name=insurer.trade_name,
            cnpj=insurer.cnpj,
            registration_number=insurer.registration_number,
            type=insurer.type.value,
            status=insurer.status.value,
            phone=insurer.phone,
            email=insurer.email,
            website=insurer.website,
            address={
                "street": insurer.address.street,
                "number": insurer.address.number,
                "complement": insurer.address.complement,
                "neighborhood": insurer.address.neighborhood,
                "city": insurer.address.city,
                "state": insurer.address.state,
                "zip_code": insurer.address.zip_code,
            },
            plans=[
                {
                    "id": str(plan.id),
                    "name": plan.name,
                    "code": plan.code,
                    "type": plan.type.value,
                    "coverage": plan.coverage,
                    "active": plan.active,
                    "monthly_price": plan.monthly_price,
                }
                for plan in insurer.plans
            ],
            logo=insurer.logo,
            contract_start_date=insurer.contract_start_date,
            contract_end_date=insurer.contract_end_date,
            notes=insurer.notes,
            created_at=insurer.created_at,
            updated_at=insurer.updated_at,
        )
    
    @staticmethod
    def _to_entity(model: InsurerModel) -> Insurer:
        """Convert database model to domain entity."""
        return Insurer(
            id=model.id,
            name=model.name,
            trade_name=model.trade_name,
            cnpj=model.cnpj,
            registration_number=model.registration_number,
            type=InsurerType(model.type),
            status=InsurerStatus(model.status),
            phone=model.phone,
            email=model.email,
            website=model.website,
            address=InsurerAddress(
                street=model.address["street"],
                number=model.address["number"],
                complement=model.address.get("complement"),
                neighborhood=model.address["neighborhood"],
                city=model.address["city"],
                state=model.address["state"],
                zip_code=model.address["zip_code"],
            ),
            plans=[
                InsurerPlan(
                    id=UUID(plan["id"]),
                    name=plan["name"],
                    code=plan["code"],
                    type=PlanType(plan["type"]),
                    coverage=plan["coverage"],
                    active=plan["active"],
                    monthly_price=plan.get("monthly_price"),
                )
                for plan in (model.plans or [])
            ],
            logo=model.logo,
            contract_start_date=model.contract_start_date,
            contract_end_date=model.contract_end_date,
            notes=model.notes,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
