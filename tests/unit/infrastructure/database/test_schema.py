from sqlalchemy import inspect
from src.infrastructure.database.models.patient_model import PatientModel

def test_patient_caregiver_id_index():
    """Verify that caregiver_id column has an index for performance optimization."""
    inspector = inspect(PatientModel)
    # Get the column object from the mapper
    column = next(c for c in inspector.columns if c.name == 'caregiver_id')

    # Check if index=True is set on the column definition
    assert column.index is True, "caregiver_id should be indexed for performance"
