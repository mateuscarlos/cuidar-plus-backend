import pytest
from unittest.mock import patch
from datetime import datetime, timedelta
from uuid import uuid4
from src.main import create_app
from src.infrastructure.database.models.patient_model import PatientModel
from src.infrastructure.database.models.user_model import UserModel

@pytest.fixture
def client(test_session):
    app = create_app()
    app.config["TESTING"] = True

    from contextlib import contextmanager

    @contextmanager
    def mock_get_db_context():
        try:
            yield test_session
        except Exception:
            pass

    with patch("src.presentation.api.v1.routes.patient_routes.get_db_context", side_effect=mock_get_db_context):
        with app.test_client() as client:
            yield client

def test_list_patients_sorting(client, test_session):
    # Setup data
    caregiver = UserModel(
        id=uuid4(),
        email="caregiver@test.com",
        password_hash="hash",
        full_name="Caregiver",
        role="caregiver"
    )
    test_session.add(caregiver)
    test_session.flush()

    # Create patients with distinct created_at times
    now = datetime.now()

    # Oldest
    p1 = PatientModel(
        id=uuid4(),
        caregiver_id=caregiver.id,
        full_name="P1 Oldest",
        cpf="111",
        date_of_birth=datetime(1950, 1, 1).date(),
        gender="M",
        address="A",
        phone="1",
        emergency_contact="E",
        emergency_phone="2",
        is_active=True,
        created_at=now - timedelta(days=2)
    )

    # Middle
    p2 = PatientModel(
        id=uuid4(),
        caregiver_id=caregiver.id,
        full_name="P2 Middle",
        cpf="222",
        date_of_birth=datetime(1950, 1, 1).date(),
        gender="F",
        address="A",
        phone="1",
        emergency_contact="E",
        emergency_phone="2",
        is_active=True,
        created_at=now - timedelta(days=1)
    )

    # Newest
    p3 = PatientModel(
        id=uuid4(),
        caregiver_id=caregiver.id,
        full_name="P3 Newest",
        cpf="333",
        date_of_birth=datetime(1950, 1, 1).date(),
        gender="M",
        address="A",
        phone="1",
        emergency_contact="E",
        emergency_phone="2",
        is_active=True,
        created_at=now
    )

    test_session.add_all([p1, p2, p3])
    test_session.commit()

    # Call endpoint
    response = client.get("/api/v1/patients/?pageSize=10")
    assert response.status_code == 200

    data = response.get_json()
    patients = data["data"]

    assert len(patients) == 3

    # Verify order: Newest (P3) -> Middle (P2) -> Oldest (P1)
    assert patients[0]["full_name"] == "P3 Newest"
    assert patients[1]["full_name"] == "P2 Middle"
    assert patients[2]["full_name"] == "P1 Oldest"
