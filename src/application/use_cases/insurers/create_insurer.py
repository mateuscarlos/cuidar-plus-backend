"""Create Insurer Use Case."""
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.domain.entities.insurer import Insurer, InsurerAddress, InsurerType
from src.domain.repositories.insurer_repository import InsurerRepository
from src.domain.services.insurer_service import InsurerDomainService
from src.shared.exceptions.application_exception import ApplicationException


@dataclass
class CreateInsurerInput:
    """Input DTO for CreateInsurer use case."""
    
    name: str
    trade_name: str
    cnpj: str
    registration_number: str
    type: str
    phone: str
    email: str
    address: dict
    website: Optional[str] = None
    logo: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class CreateInsurerOutput:
    """Output DTO for CreateInsurer use case."""
    
    id: UUID
    name: str
    trade_name: str
    cnpj: str
    status: str


class CreateInsurerUseCase:
    """
    Use Case: Create a new insurer.
    
    Business Rules:
    - Validate all required fields
    - Validate CNPJ format and check digits
    - Validate ANS registration number (6 digits)
    - Check for duplicate CNPJ
    - Check for duplicate ANS registration
    """
    
    def __init__(self, insurer_repository: InsurerRepository) -> None:
        self._insurer_repository = insurer_repository
    
    async def execute(self, input_dto: CreateInsurerInput) -> CreateInsurerOutput:
        """Execute the use case."""
        
        # Validate business rules using Domain Service
        errors = InsurerDomainService.validate_for_creation(
            name=input_dto.name,
            cnpj=input_dto.cnpj,
            registration_number=input_dto.registration_number,
            email=input_dto.email,
            phone=input_dto.phone,
        )
        
        if errors:
            raise ApplicationException(
                message="; ".join(errors),
                code="VALIDATION_ERROR",
            )
        
        # Validate CNPJ with check digits
        if not InsurerDomainService.validate_cnpj(input_dto.cnpj):
            raise ApplicationException(
                message="CNPJ inválido (dígitos verificadores incorretos)",
                code="INVALID_CNPJ",
            )
        
        # Check if CNPJ already exists
        existing = await self._insurer_repository.get_by_cnpj(input_dto.cnpj)
        if existing:
            raise ApplicationException(
                message="Já existe uma operadora cadastrada com este CNPJ",
                code="DUPLICATE_CNPJ",
            )
        
        # Check if registration number already exists
        existing_by_ans = await self._insurer_repository.get_by_registration_number(
            input_dto.registration_number
        )
        if existing_by_ans:
            raise ApplicationException(
                message="Já existe uma operadora cadastrada com este número ANS",
                code="DUPLICATE_ANS",
            )
        
        # Create address value object
        address = InsurerAddress(
            street=input_dto.address["street"],
            number=input_dto.address["number"],
            neighborhood=input_dto.address["neighborhood"],
            city=input_dto.address["city"],
            state=input_dto.address["state"],
            zip_code=input_dto.address["zip_code"],
            complement=input_dto.address.get("complement"),
        )
        
        # Create insurer entity
        insurer = Insurer.create(
            name=input_dto.name,
            trade_name=input_dto.trade_name,
            cnpj=input_dto.cnpj,
            registration_number=input_dto.registration_number,
            type=InsurerType(input_dto.type),
            phone=input_dto.phone,
            email=input_dto.email,
            address=address,
            website=input_dto.website,
            logo=input_dto.logo,
            notes=input_dto.notes,
        )
        
        # Persist
        insurer = await self._insurer_repository.create(insurer)
        
        return CreateInsurerOutput(
            id=insurer.id,
            name=insurer.name,
            trade_name=insurer.trade_name,
            cnpj=insurer.cnpj,
            status=insurer.status.value,
        )
