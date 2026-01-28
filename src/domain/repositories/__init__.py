"""Repository interfaces package."""
from .appointment_repository import AppointmentRepository
from .insurer_repository import InsurerRepository
from .inventory_item_repository import InventoryItemRepository
from .medication_repository import MedicationRepository
from .patient_repository import PatientRepository
from .provider_repository import ProviderRepository
from .report_repository import ReportRepository
from .user_repository import UserRepository

__all__ = [
    "AppointmentRepository",
    "InsurerRepository",
    "InventoryItemRepository",
    "MedicationRepository",
    "PatientRepository",
    "ProviderRepository",
    "ReportRepository",
    "UserRepository",
]
