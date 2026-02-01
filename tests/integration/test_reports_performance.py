import pytest
from unittest.mock import patch
from datetime import datetime, timedelta
from uuid import uuid4
from src.main import create_app
from src.infrastructure.database.models.patient_model import PatientModel
from src.infrastructure.database.models.medication_model import MedicationModel
from src.infrastructure.database.models.appointment_model import AppointmentModel
from src.infrastructure.database.models.user_model import UserModel

@pytest.fixture
def client(test_session):
    app = create_app()
    app.config["TESTING"] = True

    # We need to patch get_db_context to use our test_session
    from contextlib import contextmanager

    @contextmanager
    def mock_get_db_context():
        try:
            yield test_session
        except Exception:
            pass

    with patch("src.presentation.api.v1.routes.reports_routes.get_db_context", side_effect=mock_get_db_context):
        with app.test_client() as client:
            yield client

def test_get_summary_performance(client, test_session):
    # Setup data
    # Create a caregiver
    caregiver = UserModel(
        id=uuid4(),
        email="caregiver@test.com",
        password_hash="hash",
        full_name="Caregiver",
        role="caregiver"
    )
    test_session.add(caregiver)
    test_session.flush()

    # Create Patients (3 total, 2 active)
    p1 = PatientModel(id=uuid4(), caregiver_id=caregiver.id, full_name="P1", cpf="111", date_of_birth=datetime(1950, 1, 1).date(), gender="M", address="A", phone="1", emergency_contact="E", emergency_phone="2", is_active=True)
    p2 = PatientModel(id=uuid4(), caregiver_id=caregiver.id, full_name="P2", cpf="222", date_of_birth=datetime(1950, 1, 1).date(), gender="F", address="A", phone="1", emergency_contact="E", emergency_phone="2", is_active=True)
    p3 = PatientModel(id=uuid4(), caregiver_id=caregiver.id, full_name="P3", cpf="333", date_of_birth=datetime(1950, 1, 1).date(), gender="M", address="A", phone="1", emergency_contact="E", emergency_phone="2", is_active=False)
    test_session.add_all([p1, p2, p3])

    # Create Medications (2 total, 1 active)
    m1 = MedicationModel(id=uuid4(), patient_id=p1.id, name="M1", dosage="D", frequency="F", schedule_times=[], start_date=datetime.now(), is_active=True)
    m2 = MedicationModel(id=uuid4(), patient_id=p1.id, name="M2", dosage="D", frequency="F", schedule_times=[], start_date=datetime.now(), is_active=False)
    test_session.add_all([m1, m2])

    # Create Appointments (2 total, 1 upcoming)
    now = datetime.now()
    future = now + timedelta(days=1)
    past = now - timedelta(days=1)

    a1 = AppointmentModel(id=uuid4(), patient_id=p1.id, title="A1", appointment_date=future, duration_minutes=30, location="L", status="scheduled")
    a2 = AppointmentModel(id=uuid4(), patient_id=p1.id, title="A2", appointment_date=past, duration_minutes=30, location="L", status="completed")
    test_session.add_all([a1, a2])

    test_session.commit()

    # Run the test
    response = client.get("/api/v1/reports/summary")

    assert response.status_code == 200
    data = response.get_json()

    assert data["patients"]["total"] == 3
    assert data["patients"]["active"] == 2
    assert data["patients"]["inactive"] == 1

    assert data["medications"]["total"] == 2
    assert data["medications"]["active"] == 1
    assert data["medications"]["inactive"] == 1

    assert data["appointments"]["total"] == 2
    assert data["appointments"]["upcoming"] == 1
    assert data["appointments"]["completed"] == 1
