
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask

# Import the app factory
from src.main import create_app

# Import the settings module used by auth middleware
import src.presentation.api.middlewares.auth_middleware as auth_middleware

class TestPatientSecurity(unittest.TestCase):
    def setUp(self):
        # Patch the settings object in auth_middleware to force production mode
        # This ensures the authentication check is NOT bypassed
        self.settings_patcher = patch.object(auth_middleware.settings, 'FLASK_ENV', 'production')
        self.settings_patcher.start()

        # Patch get_db_context to avoid database dependency
        self.db_patcher = patch('src.infrastructure.database.session.get_db_context')
        self.mock_db_context = self.db_patcher.start()

        # Setup mock session
        self.mock_session = MagicMock()
        self.mock_db_context.return_value.__enter__.return_value = self.mock_session

        # Create the app
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def tearDown(self):
        self.settings_patcher.stop()
        self.db_patcher.stop()

    def test_list_patients_unauthenticated(self):
        """Test listing patients without authentication (should be 401)."""
        # Mock query results to avoid errors if auth is bypassed (vulnerability check)
        self.mock_session.query.return_value.offset.return_value.limit.return_value.all.return_value = []
        self.mock_session.query.return_value.count.return_value = 0

        response = self.client.get('/api/v1/patients/')

        # If vulnerable, it returns 200. If secure, it returns 401.
        # We assert 401 because that's the desired state.
        self.assertEqual(response.status_code, 401, "Endpoint /api/v1/patients/ should require authentication")

    def test_create_patient_unauthenticated(self):
        """Test creating patient without authentication (should be 401)."""
        data = {
            "caregiver_id": "00000000-0000-0000-0000-000000000000",
            "full_name": "Test Patient",
            "cpf": "123.456.789-00",
            "date_of_birth": "1990-01-01",
            "gender": "M",
            "address": "Test St",
            "phone": "1234567890",
            "emergency_contact": "Emergency",
            "emergency_phone": "0987654321"
        }

        response = self.client.post('/api/v1/patients/', json=data)
        self.assertEqual(response.status_code, 401, "Endpoint POST /api/v1/patients/ should require authentication")

    def test_list_patients_by_caregiver_unauthenticated(self):
        """Test listing patients by caregiver without authentication (should be 401)."""
        caregiver_id = "00000000-0000-0000-0000-000000000000"

        # Mock query results
        self.mock_session.query.return_value.filter.return_value.all.return_value = []
        self.mock_session.query.return_value.count.return_value = 0

        response = self.client.get(f'/api/v1/patients/caregiver/{caregiver_id}')
        self.assertEqual(response.status_code, 401, "Endpoint /api/v1/patients/caregiver/<id> should require authentication")

if __name__ == '__main__':
    unittest.main()
