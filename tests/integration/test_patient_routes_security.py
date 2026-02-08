import pytest
from unittest.mock import MagicMock, patch
from src.main import create_app

@pytest.fixture
def mock_settings():
    with patch("src.presentation.api.middlewares.auth_middleware.settings") as mock_settings:
        mock_settings.FLASK_ENV = "production"
        yield mock_settings

def test_list_patients_unauthenticated_access(mock_settings):
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    with patch("src.presentation.api.v1.routes.patient_routes.get_db_context") as mock_db:
        mock_session = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_session

        # Mock the query chain to return empty list if it gets that far
        mock_session.query.return_value.offset.return_value.limit.return_value.all.return_value = []
        mock_session.query.return_value.count.return_value = 0

        response = client.get("/api/v1/patients/")

        if response.status_code == 200:
            pytest.fail("VULNERABLE: /api/v1/patients/ is accessible without authentication!")

        assert response.status_code == 401, f"Expected 401, got {response.status_code}"

def test_create_patient_unauthenticated_access(mock_settings):
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    response = client.post("/api/v1/patients/", json={
        "full_name": "Test Patient",
        "cpf": "123.456.789-00"
    })

    if response.status_code != 401:
        pytest.fail(f"VULNERABLE: /api/v1/patients/ (POST) does not require authentication! Status: {response.status_code}")

def test_list_patients_by_caregiver_unauthenticated_access(mock_settings):
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()
    caregiver_id = "123e4567-e89b-12d3-a456-426614174000"

    with patch("src.presentation.api.v1.routes.patient_routes.get_db_context") as mock_db:
        mock_session = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_session

        # Mock empty result
        mock_session.query.return_value.filter.return_value.all.return_value = []

        response = client.get(f"/api/v1/patients/caregiver/{caregiver_id}")

        if response.status_code != 401:
             pytest.fail(f"VULNERABLE: /api/v1/patients/caregiver/{caregiver_id} does not require authentication! Status: {response.status_code}")
