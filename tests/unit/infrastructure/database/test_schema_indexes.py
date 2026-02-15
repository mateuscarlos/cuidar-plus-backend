import pytest
from sqlalchemy import inspect
# Import models to ensure they are registered with Base
from src.infrastructure.database.models.patient_model import PatientModel
from src.infrastructure.database.models.appointment_model import AppointmentModel
from src.infrastructure.database.models.medication_model import MedicationModel

def get_indexes(engine, table_name):
    inspector = inspect(engine)
    return inspector.get_indexes(table_name)

def test_patient_foreign_key_indexes(test_engine):
    indexes = get_indexes(test_engine, "patients")

    # Check if caregiver_id is indexed
    is_caregiver_indexed = False
    for idx in indexes:
        if 'caregiver_id' in idx['column_names']:
            is_caregiver_indexed = True
            break

    assert is_caregiver_indexed, "caregiver_id should be indexed in patients"

def test_appointment_foreign_key_indexes(test_engine):
    indexes = get_indexes(test_engine, "appointments")
    is_patient_indexed = False
    for idx in indexes:
        if 'patient_id' in idx['column_names']:
            is_patient_indexed = True
            break

    assert is_patient_indexed, "patient_id should be indexed in appointments"

def test_medication_foreign_key_indexes(test_engine):
    indexes = get_indexes(test_engine, "medications")
    is_patient_indexed = False
    for idx in indexes:
        if 'patient_id' in idx['column_names']:
            is_patient_indexed = True
            break

    assert is_patient_indexed, "patient_id should be indexed in medications"
