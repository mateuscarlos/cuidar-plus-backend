"""Insurer Entity (Operadora de Saúde)."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class InsurerStatus(str, Enum):
    """Insurer Status."""
    
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"


class InsurerType(str, Enum):
    """Insurer Type."""
    
    MEDICINA_GRUPO = "MEDICINA_GRUPO"  # Medicina de Grupo
    COOPERATIVA = "COOPERATIVA"  # Cooperativa Médica
    AUTOGESTAO = "AUTOGESTAO"  # Autogestão
    FILANTROPIA = "FILANTROPIA"  # Filantropia


class PlanType(str, Enum):
    """Plan Type."""
    
    INDIVIDUAL = "INDIVIDUAL"
    EMPRESARIAL = "EMPRESARIAL"
    COLETIVO_ADESAO = "COLETIVO_ADESAO"


@dataclass
class InsurerPlan:
    """Insurer Plan."""
    
    id: UUID
    name: str
    code: str
    type: PlanType
    coverage: list[str]
    active: bool
    monthly_price: Optional[float] = None


@dataclass
class InsurerAddress:
    """Insurer Address."""
    
    street: str
    number: str
    neighborhood: str
    city: str
    state: str
    zip_code: str
    complement: Optional[str] = None


@dataclass
class Insurer:
    """
    Insurer Entity (Operadora de Saúde).
    
    Represents health insurance companies like SulAmerica, Amil, Unimed, etc.
    """
    
    id: UUID
    name: str
    trade_name: str
    cnpj: str
    registration_number: str  # Número de registro na ANS
    type: InsurerType
    status: InsurerStatus
    phone: str
    email: str
    address: InsurerAddress
    plans: list[InsurerPlan] = field(default_factory=list)
    website: Optional[str] = None
    logo: Optional[str] = None
    contract_start_date: Optional[datetime] = None
    contract_end_date: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    @classmethod
    def create(
        cls,
        name: str,
        trade_name: str,
        cnpj: str,
        registration_number: str,
        type: InsurerType,
        phone: str,
        email: str,
        address: InsurerAddress,
        website: Optional[str] = None,
        plans: Optional[list[InsurerPlan]] = None,
        logo: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> "Insurer":
        """
        Create a new Insurer.
        
        Args:
            name: Official name
            trade_name: Trading name
            cnpj: CNPJ number
            registration_number: ANS registration number
            type: Insurer type
            phone: Contact phone
            email: Contact email
            address: Address information
            website: Website URL
            plans: List of plans offered
            logo: Logo URL
            notes: Additional notes
            
        Returns:
            New Insurer instance
        """
        cls._validate_cnpj(cnpj)
        cls._validate_email(email)
        
        return cls(
            id=uuid4(),
            name=name,
            trade_name=trade_name,
            cnpj=cnpj,
            registration_number=registration_number,
            type=type,
            status=InsurerStatus.ACTIVE,
            phone=phone,
            email=email,
            address=address,
            website=website,
            plans=plans or [],
            logo=logo,
            notes=notes,
        )
    
    def update(
        self,
        name: Optional[str] = None,
        trade_name: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        website: Optional[str] = None,
        status: Optional[InsurerStatus] = None,
        address: Optional[InsurerAddress] = None,
        plans: Optional[list[InsurerPlan]] = None,
        logo: Optional[str] = None,
        contract_start_date: Optional[datetime] = None,
        contract_end_date: Optional[datetime] = None,
        notes: Optional[str] = None,
    ) -> None:
        """Update insurer information."""
        if name is not None:
            self.name = name
        if trade_name is not None:
            self.trade_name = trade_name
        if phone is not None:
            self.phone = phone
        if email is not None:
            self._validate_email(email)
            self.email = email
        if website is not None:
            self.website = website
        if status is not None:
            self.status = status
        if address is not None:
            self.address = address
        if plans is not None:
            self.plans = plans
        if logo is not None:
            self.logo = logo
        if contract_start_date is not None:
            self.contract_start_date = contract_start_date
        if contract_end_date is not None:
            self.contract_end_date = contract_end_date
        if notes is not None:
            self.notes = notes
        
        self.updated_at = datetime.utcnow()
    
    def activate(self) -> None:
        """Activate insurer."""
        self.status = InsurerStatus.ACTIVE
        self.updated_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """Deactivate insurer."""
        self.status = InsurerStatus.INACTIVE
        self.updated_at = datetime.utcnow()
    
    def suspend(self) -> None:
        """Suspend insurer."""
        self.status = InsurerStatus.SUSPENDED
        self.updated_at = datetime.utcnow()
    
    def add_plan(self, plan: InsurerPlan) -> None:
        """Add a new plan."""
        self.plans.append(plan)
        self.updated_at = datetime.utcnow()
    
    def remove_plan(self, plan_id: UUID) -> None:
        """Remove a plan."""
        self.plans = [p for p in self.plans if p.id != plan_id]
        self.updated_at = datetime.utcnow()
    
    @staticmethod
    def _validate_cnpj(cnpj: str) -> None:
        """Validate CNPJ format (basic validation)."""
        cnpj_numbers = ''.join(filter(str.isdigit, cnpj))
        if len(cnpj_numbers) != 14:
            raise ValueError("CNPJ deve conter 14 dígitos")
    
    @staticmethod
    def _validate_email(email: str) -> None:
        """Validate email format (basic validation)."""
        if '@' not in email or '.' not in email:
            raise ValueError("Email inválido")
