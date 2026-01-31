import pytest

from src.main import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_root_json(client):
    """Test root endpoint returns JSON by default or when requested."""
    # Test explicitly requesting JSON
    response = client.get("/", headers={"Accept": "application/json"})
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data["service"] == "Cuidar Plus API"

    # Test default (no accept header or */*) - Expect JSON for API stability
    response = client.get("/", headers={"Accept": "*/*"})
    assert response.status_code == 200
    assert response.is_json

def test_root_html(client):
    """Test root endpoint returns HTML when requested."""
    # Browsers send text/html
    response = client.get("/", headers={"Accept": "text/html"})
    assert response.status_code == 200
    assert "text/html" in response.content_type
    assert b"<!DOCTYPE html>" in response.data
    assert b"Cuidar Plus API" in response.data
    assert b"v1" in response.data
