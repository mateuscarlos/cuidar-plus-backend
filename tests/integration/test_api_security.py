import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Set environment variables BEFORE importing src
os.environ['SECRET_KEY'] = 'test'
os.environ['JWT_SECRET_KEY'] = 'test_jwt'
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

# Patch create_engine to avoid SQLite errors with pool params
with patch('sqlalchemy.create_engine') as mock_create_engine:
    from src.main import create_app
    from src.infrastructure.security.jwt_handler import JWTHandler

class TestSecurityFix(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.jwt_handler = JWTHandler()
        self.valid_token = self.jwt_handler.create_access_token(subject="user123")
        self.headers = {"Authorization": f"Bearer {self.valid_token}"}

    @patch('src.presentation.api.v1.routes.patient_routes.get_db_context')
    def test_patients_endpoints_protected(self, mock_get_db_context):
        """Test that patient endpoints are protected (401 without token)."""
        endpoints = [
            ('GET', '/api/v1/patients/'),
        ]

        for method, url in endpoints:
            with self.subTest(method=method, url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 401, f"{method} {url} should return 401 without token")

    @patch('src.presentation.api.v1.routes.patient_routes.get_db_context')
    def test_patients_endpoints_accessible_with_token(self, mock_get_db_context):
        """Test that patient endpoints are accessible with valid token."""
        # Setup mock DB
        mock_session = MagicMock()
        mock_ctx = MagicMock()
        mock_ctx.__enter__.return_value = mock_session
        mock_get_db_context.return_value = mock_ctx

        # Mock query results to avoid 500 error
        mock_query = mock_session.query.return_value
        mock_query.offset.return_value.limit.return_value.all.return_value = []
        mock_query.count.return_value = 0

        response = self.client.get('/api/v1/patients/', headers=self.headers)

        # Should be 200 OK
        self.assertEqual(response.status_code, 200, "Should be accessible with valid token")

        # Should have called get_db_context
        mock_get_db_context.assert_called()

if __name__ == '__main__':
    unittest.main()
