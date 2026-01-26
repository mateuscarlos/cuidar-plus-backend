"""SQLAlchemy Patient Repository Implementation."""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.domain.entities.patient import Patient
from src.domain.repositories.patient_repository import PatientRepository
from src.domain.value_objects.cpf import CPF
from src.infrastructure.database.models.patient_model import PatientModel


class SQLAlchemyPatientRepository(PatientRepository):
    """SQLAlchemy implementation of PatientRepository."""
    
    def __init__(self, session: Session) -> None:
        self._session = session
    
    def save(self, patient: Patient) -> Patient:
        """Persist patient to database."""
        patient_model = self._to_model(patient)
        self._session.merge(patient_model)
        self._session.flush()
        return self._to_entity(patient_model)
    
    def find_by_id(self, patient_id: UUID) -> Optional[Patient]:
        """Find patient by ID."""
        patient_model = self._session.query(PatientModel).filter(
            PatientModel.id == patient_id
        ).first()
        
        return self._to_entity(patient_model) if patient_model else None
    
    def find_by_caregiver(self, caregiver_id: UUID) -> list[Patient]:
        """Find all patients for a specific caregiver."""
        patient_models = self._session.query(PatientModel).filter(
            PatientModel.caregiver_id == caregiver_id
        ).all()
        
        return [self._to_entity(model) for model in patient_models]
    
    def delete(self, patient_id: UUID) -> None:
        """Delete patient by ID."""
        self._session.query(PatientModel).filter(
            PatientModel.id == patient_id
        ).delete()
    
    def find_all(self, skip: int = 0, limit: int = 100) -> list[Patient]:
        """Find all patients with pagination."""
        patient_models = self._session.query(PatientModel).offset(skip).limit(limit).all()
        return [self._to_entity(model) for model in patient_models]
    
    @staticmethod
    def _to_model(patient: Patient) -> PatientModel:
        """Convert domain entity to database model."""
        return PatientModel(
            id=patient.id,
            caregiver_id=patient.caregiver_id,
            full_name=patient.full_name,
            cpf=patient.cpf.value,
            date_of_birth=patient.date_of_birth,
            gender=patient.gender,
            address=patient.address,
            phone=patient.phone,
            emergency_contact=patient.emergency_contact,
            emergency_phone=patient.emergency_phone,
            medical_conditions=patient.medical_conditions,
            allergies=patient.allergies,
            observations=patient.observations,
            is_active=patient.is_active,
            created_at=patient.created_at,
            updated_at=patient.updated_at,
        )
    
    @staticmethod
    def _to_entity(model: PatientModel) -> Patient:
        """Convert database model to domain entity."""
        return Patient(
            id=model.id,
            caregiver_id=model.caregiver_id,
            full_name=model.full_name,
            cpf=CPF(model.cpf),
            date_of_birth=model.date_of_birth,
            gender=model.gender,
            address=model.address,
            phone=model.phone,
            emergency_contact=model.emergency_contact,
            emergency_phone=model.emergency_phone,
            medical_conditions=model.medical_conditions,
            allergies=model.allergies,
            observations=model.observations,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
