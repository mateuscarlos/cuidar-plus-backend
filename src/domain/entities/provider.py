"""Provider Entity (Prestadora de Serviços)."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class ProviderStatus(str, Enum):
    """Provider Status."""
    
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    PENDING_APPROVAL = "PENDING_APPROVAL"


class ProviderType(str, Enum):
    """Provider Type."""
    
    HOSPITAL = "HOSPITAL"
    CLINICA = "CLINICA"
    LABORATORIO = "LABORATORIO"
    COOPERATIVA = "COOPERATIVA"
    CONSULTORIO = "CONSULTORIO"
    CENTRO_DIAGNOSTICO = "CENTRO_DIAGNOSTICO"
    HOME_CARE = "HOME_CARE"


class ProviderSpecialty(str, Enum):
    """Provider Specialty."""
    
    CARDIOLOGIA = "CARDIOLOGIA"
    ORTOPEDIA = "ORTOPEDIA"
    PEDIATRIA = "PEDIATRIA"
    GINECOLOGIA = "GINECOLOGIA"
    NEUROLOGIA = "NEUROLOGIA"
    PSIQUIATRIA = "PSIQUIATRIA"
    DERMATOLOGIA = "DERMATOLOGIA"
    OFTALMOLOGIA = "OFTALMOLOGIA"
    ONCOLOGIA = "ONCOLOGIA"
    GERAL = "GERAL"


class CredentialType(str, Enum):
    """Credential Type."""
    
    CRM = "CRM"
    CNES = "CNES"
    CNPJ = "CNPJ"
    CPF = "CPF"
    OUTROS = "OUTROS"


@dataclass
class ProviderCredential:
    """Provider Credential."""
    
    type: CredentialType
    number: str
    state: Optional[str] = None
    expiration_date: Optional[datetime] = None


@dataclass
class ProviderService:
    """Provider Service."""
    
    id: UUID
    name: str
    code: str
    price: float
    description: Optional[str] = None
    duration: Optional[int] = None  # em minutos
    active: bool = True


@dataclass
class ProviderAddress:
    """Provider Address."""
    
    street: str
    number: str
    neighborhood: str
    city: str
    state: str
    zip_code: str
    complement: Optional[str] = None


@dataclass
class WorkingHours:
    """Working Hours."""
    
    monday: Optional[str] = None
    tuesday: Optional[str] = None
    wednesday: Optional[str] = None
    thursday: Optional[str] = None
    friday: Optional[str] = None
    saturday: Optional[str] = None
    sunday: Optional[str] = None


@dataclass
class Provider:
    """
    Provider Entity (Prestadora de Serviços).
    
    Represents health service providers like hospitals, clinics, cooperatives, etc.
    """
    
    id: UUID
    name: str
    trade_name: str
    type: ProviderType
    status: ProviderStatus
    document: str  # CNPJ ou CPF
    credentials: list[ProviderCredential]
    specialties: list[ProviderSpecialty]
    phone: str
    email: str
    address: ProviderAddress
    services: list[ProviderService] = field(default_factory=list)
    accepted_insurers: list[UUID] = field(default_factory=list)
    website: Optional[str] = None
    working_hours: Optional[WorkingHours] = None
    logo: Optional[str] = None
    capacity: Optional[int] = None
    has_emergency: bool = False
    rating: Optional[float] = None
    notes: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    @classmethod
    def create(
        cls,
        name: str,
        trade_name: str,
        type: ProviderType,
        document: str,
        credentials: list[ProviderCredential],
        specialties: list[ProviderSpecialty],
        phone: str,
        email: str,
        address: ProviderAddress,
        website: Optional[str] = None,
        working_hours: Optional[WorkingHours] = None,
        services: Optional[list[ProviderService]] = None,
        accepted_insurers: Optional[list[UUID]] = None,
        logo: Optional[str] = None,
        capacity: Optional[int] = None,
        has_emergency: bool = False,
        notes: Optional[str] = None,
    ) -> "Provider":
        """
        Create a new Provider.
        
        Args:
            name: Official name
            trade_name: Trading name
            type: Provider type
            document: CNPJ or CPF
            credentials: Professional credentials
            specialties: Medical specialties
            phone: Contact phone
            email: Contact email
            address: Address information
            website: Website URL
            working_hours: Working hours schedule
            services: Services offered
            accepted_insurers: List of accepted insurer IDs
            logo: Logo URL
            capacity: Service capacity
            has_emergency: Has emergency service
            notes: Additional notes
            
        Returns:
            New Provider instance
        """
        cls._validate_document(document)
        cls._validate_email(email)
        
        return cls(
            id=uuid4(),
            name=name,
            trade_name=trade_name,
            type=type,
            status=ProviderStatus.PENDING_APPROVAL,
            document=document,
            credentials=credentials,
            specialties=specialties,
            phone=phone,
            email=email,
            address=address,
            website=website,
            working_hours=working_hours,
            services=services or [],
            accepted_insurers=accepted_insurers or [],
            logo=logo,
            capacity=capacity,
            has_emergency=has_emergency,
            notes=notes,
        )
    
    def update(
        self,
        name: Optional[str] = None,
        trade_name: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        website: Optional[str] = None,
        status: Optional[ProviderStatus] = None,
        specialties: Optional[list[ProviderSpecialty]] = None,
        address: Optional[ProviderAddress] = None,
        working_hours: Optional[WorkingHours] = None,
        services: Optional[list[ProviderService]] = None,
        accepted_insurers: Optional[list[UUID]] = None,
        logo: Optional[str] = None,
        capacity: Optional[int] = None,
        has_emergency: Optional[bool] = None,
        rating: Optional[float] = None,
        notes: Optional[str] = None,
    ) -> None:
        """Update provider information."""
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
        if specialties is not None:
            self.specialties = specialties
        if address is not None:
            self.address = address
        if working_hours is not None:
            self.working_hours = working_hours
        if services is not None:
            self.services = services
        if accepted_insurers is not None:
            self.accepted_insurers = accepted_insurers
        if logo is not None:
            self.logo = logo
        if capacity is not None:
            self.capacity = capacity
        if has_emergency is not None:
            self.has_emergency = has_emergency
        if rating is not None:
            if not 0 <= rating <= 5:
                raise ValueError("Rating deve estar entre 0 e 5")
            self.rating = rating
        if notes is not None:
            self.notes = notes
        
        self.updated_at = datetime.utcnow()
    
    def activate(self) -> None:
        """Activate provider."""
        self.status = ProviderStatus.ACTIVE
        self.updated_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """Deactivate provider."""
        self.status = ProviderStatus.INACTIVE
        self.updated_at = datetime.utcnow()
    
    def suspend(self) -> None:
        """Suspend provider."""
        self.status = ProviderStatus.SUSPENDED
        self.updated_at = datetime.utcnow()
    
    def approve(self) -> None:
        """Approve pending provider."""
        if self.status != ProviderStatus.PENDING_APPROVAL:
            raise ValueError("Apenas prestadores pendentes podem ser aprovados")
        self.status = ProviderStatus.ACTIVE
        self.updated_at = datetime.utcnow()
    
    def add_service(self, service: ProviderService) -> None:
        """Add a new service."""
        self.services.append(service)
        self.updated_at = datetime.utcnow()
    
    def remove_service(self, service_id: UUID) -> None:
        """Remove a service."""
        self.services = [s for s in self.services if s.id != service_id]
        self.updated_at = datetime.utcnow()
    
    def add_insurer(self, insurer_id: UUID) -> None:
        """Add accepted insurer."""
        if insurer_id not in self.accepted_insurers:
            self.accepted_insurers.append(insurer_id)
            self.updated_at = datetime.utcnow()
    
    def remove_insurer(self, insurer_id: UUID) -> None:
        """Remove accepted insurer."""
        if insurer_id in self.accepted_insurers:
            self.accepted_insurers.remove(insurer_id)
            self.updated_at = datetime.utcnow()
    
    @staticmethod
    def _validate_document(document: str) -> None:
        """Validate document format (basic validation)."""
        doc_numbers = ''.join(filter(str.isdigit, document))
        if len(doc_numbers) not in [11, 14]:
            raise ValueError("Documento deve conter 11 (CPF) ou 14 (CNPJ) dígitos")
    
    @staticmethod
    def _validate_email(email: str) -> None:
        """Validate email format (basic validation)."""
        if '@' not in email or '.' not in email:
            raise ValueError("Email inválido")
