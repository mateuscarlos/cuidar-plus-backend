"""SQLAlchemy Provider Repository Implementation."""
from typing import Optional
from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.domain.entities.provider import (
    CredentialType,
    Provider,
    ProviderAddress,
    ProviderCredential,
    ProviderService,
    ProviderSpecialty,
    ProviderStatus,
    ProviderType,
    WorkingHours,
)
from src.domain.repositories.provider_repository import ProviderRepository
from src.infrastructure.database.models.provider_model import ProviderModel


class SQLAlchemyProviderRepository(ProviderRepository):
    """SQLAlchemy implementation of ProviderRepository."""
    
    def __init__(self, session: Session) -> None:
        self._session = session
    
    async def create(self, provider: Provider) -> Provider:
        """Create a new provider."""
        provider_model = self._to_model(provider)
        self._session.add(provider_model)
        self._session.flush()
        return self._to_entity(provider_model)
    
    async def get_by_id(self, provider_id: UUID) -> Optional[Provider]:
        """Get provider by ID."""
        provider_model = self._session.query(ProviderModel).filter(
            ProviderModel.id == provider_id
        ).first()
        
        return self._to_entity(provider_model) if provider_model else None
    
    async def get_by_document(self, document: str) -> Optional[Provider]:
        """Get provider by document."""
        doc_numbers = ''.join(filter(str.isdigit, document))
        provider_model = self._session.query(ProviderModel).filter(
            ProviderModel.document == doc_numbers
        ).first()
        
        return self._to_entity(provider_model) if provider_model else None
    
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
        """List providers with filters."""
        query = self._session.query(ProviderModel)
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    ProviderModel.name.ilike(search_filter),
                    ProviderModel.trade_name.ilike(search_filter),
                    ProviderModel.document.like(search_filter),
                )
            )
        
        if type:
            query = query.filter(ProviderModel.type == type.value)
        
        if status:
            query = query.filter(ProviderModel.status == status.value)
        
        # TODO: Implement specialty filter with JSON query
        # TODO: Implement city/state filter with JSON query
        # TODO: Implement accepts_insurer filter with JSON query
        
        if has_emergency is not None:
            query = query.filter(ProviderModel.has_emergency == has_emergency)
        
        total = query.count()
        providers = query.offset(skip).limit(limit).all()
        
        return [self._to_entity(model) for model in providers], total
    
    async def update(self, provider: Provider) -> Provider:
        """Update a provider."""
        provider_model = self._to_model(provider)
        self._session.merge(provider_model)
        self._session.flush()
        return self._to_entity(provider_model)
    
    async def delete(self, provider_id: UUID) -> bool:
        """Delete a provider."""
        result = self._session.query(ProviderModel).filter(
            ProviderModel.id == provider_id
        ).delete()
        self._session.flush()
        return result > 0
    
    async def get_pending_approval(self, limit: int = 100) -> list[Provider]:
        """Get providers pending approval."""
        providers = self._session.query(ProviderModel).filter(
            ProviderModel.status == ProviderStatus.PENDING_APPROVAL.value
        ).limit(limit).all()
        
        return [self._to_entity(model) for model in providers]
    
    @staticmethod
    def _to_model(provider: Provider) -> ProviderModel:
        """Convert domain entity to database model."""
        return ProviderModel(
            id=provider.id,
            name=provider.name,
            trade_name=provider.trade_name,
            type=provider.type.value,
            status=provider.status.value,
            document=provider.document,
            credentials=[
                {
                    "type": cred.type.value,
                    "number": cred.number,
                    "state": cred.state,
                    "expiration_date": cred.expiration_date.isoformat() if cred.expiration_date else None,
                }
                for cred in provider.credentials
            ],
            specialties=[spec.value for spec in provider.specialties],
            phone=provider.phone,
            email=provider.email,
            website=provider.website,
            address={
                "street": provider.address.street,
                "number": provider.address.number,
                "complement": provider.address.complement,
                "neighborhood": provider.address.neighborhood,
                "city": provider.address.city,
                "state": provider.address.state,
                "zip_code": provider.address.zip_code,
            },
            working_hours={
                "monday": provider.working_hours.monday if provider.working_hours else None,
                "tuesday": provider.working_hours.tuesday if provider.working_hours else None,
                "wednesday": provider.working_hours.wednesday if provider.working_hours else None,
                "thursday": provider.working_hours.thursday if provider.working_hours else None,
                "friday": provider.working_hours.friday if provider.working_hours else None,
                "saturday": provider.working_hours.saturday if provider.working_hours else None,
                "sunday": provider.working_hours.sunday if provider.working_hours else None,
            } if provider.working_hours else None,
            services=[
                {
                    "id": str(svc.id),
                    "name": svc.name,
                    "code": svc.code,
                    "price": svc.price,
                    "description": svc.description,
                    "duration": svc.duration,
                    "active": svc.active,
                }
                for svc in provider.services
            ],
            accepted_insurers=[str(ins_id) for ins_id in provider.accepted_insurers],
            logo=provider.logo,
            capacity=provider.capacity,
            has_emergency=provider.has_emergency,
            rating=provider.rating,
            notes=provider.notes,
            created_at=provider.created_at,
            updated_at=provider.updated_at,
        )
    
    @staticmethod
    def _to_entity(model: ProviderModel) -> Provider:
        """Convert database model to domain entity."""
        from datetime import datetime
        
        return Provider(
            id=model.id,
            name=model.name,
            trade_name=model.trade_name,
            type=ProviderType(model.type),
            status=ProviderStatus(model.status),
            document=model.document,
            credentials=[
                ProviderCredential(
                    type=CredentialType(cred["type"]),
                    number=cred["number"],
                    state=cred.get("state"),
                    expiration_date=datetime.fromisoformat(cred["expiration_date"]) if cred.get("expiration_date") else None,
                )
                for cred in model.credentials
            ],
            specialties=[ProviderSpecialty(spec) for spec in model.specialties],
            phone=model.phone,
            email=model.email,
            website=model.website,
            address=ProviderAddress(
                street=model.address["street"],
                number=model.address["number"],
                complement=model.address.get("complement"),
                neighborhood=model.address["neighborhood"],
                city=model.address["city"],
                state=model.address["state"],
                zip_code=model.address["zip_code"],
            ),
            working_hours=WorkingHours(
                monday=model.working_hours.get("monday") if model.working_hours else None,
                tuesday=model.working_hours.get("tuesday") if model.working_hours else None,
                wednesday=model.working_hours.get("wednesday") if model.working_hours else None,
                thursday=model.working_hours.get("thursday") if model.working_hours else None,
                friday=model.working_hours.get("friday") if model.working_hours else None,
                saturday=model.working_hours.get("saturday") if model.working_hours else None,
                sunday=model.working_hours.get("sunday") if model.working_hours else None,
            ) if model.working_hours else None,
            services=[
                ProviderService(
                    id=UUID(svc["id"]),
                    name=svc["name"],
                    code=svc["code"],
                    price=svc["price"],
                    description=svc.get("description"),
                    duration=svc.get("duration"),
                    active=svc["active"],
                )
                for svc in (model.services or [])
            ],
            accepted_insurers=[UUID(ins_id) for ins_id in (model.accepted_insurers or [])],
            logo=model.logo,
            capacity=model.capacity,
            has_emergency=model.has_emergency,
            rating=model.rating,
            notes=model.notes,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
