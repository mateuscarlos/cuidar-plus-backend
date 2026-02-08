import pytest
from unittest.mock import MagicMock, patch
from src.main import create_app

def test_list_patients_unauthenticated_access():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    with patch("src.presentation.api.v1.routes.patient_routes.get_db_context") as mock_db:
        mock_session = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_session

        # Mock query
        mock_session.query.return_value.offset.return_value.limit.return_value.all.return_value = []
        mock_session.query.return_value.count.return_value = 0

        response = client.get("/api/v1/patients/")

        if response.status_code == 200:
            pytest.fail("VULNERABLE: /api/v1/patients/ is accessible without authentication!")

        assert response.status_code == 401, f"Expected 401, got {response.status_code}"

def test_create_patient_unauthenticated_access():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    payload = {
        "caregiver_id": "123e4567-e89b-12d3-a456-426614174000",
        "full_name": "Test Patient",
        "cpf": "123.456.789-00",
        "date_of_birth": "1990-01-01",
        "gender": "M",
        "address": "Street 1",
        "phone": "123456789",
        "emergency_contact": "Mom",
        "emergency_phone": "987654321"
    }

    with patch("src.presentation.api.v1.routes.patient_routes.get_db_context") as mock_db:
        mock_session = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_session

        response = client.post("/api/v1/patients/", json=payload)

        if response.status_code == 201 or response.status_code == 200:
            pytest.fail("VULNERABLE: /api/v1/patients/ (POST) is accessible without authentication!")

        # We expect 401. If we get 400 or 500 because of mocking issues, it's still "authenticated" in a sense (or at least processing reached logic),
        # but for this test we explicitly want the auth middleware to reject it first.
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"

def test_list_patients_by_caregiver_unauthenticated_access():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    caregiver_id = "123e4567-e89b-12d3-a456-426614174000"

    with patch("src.presentation.api.v1.routes.patient_routes.get_db_context") as mock_db:
        mock_session = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_session

        # Mock use case
        with patch("src.presentation.api.v1.routes.patient_routes.ListPatientsByCaregiverUseCase") as mock_use_case:
             mock_use_case.return_value.execute.return_value.patients = []
             mock_use_case.return_value.execute.return_value.total = 0

             response = client.get(f"/api/v1/patients/caregiver/{caregiver_id}")

             if response.status_code == 200:
                 pytest.fail(f"VULNERABLE: /api/v1/patients/caregiver/{caregiver_id} is accessible without authentication!")

             assert response.status_code == 401, f"Expected 401, got {response.status_code}"
