
import pytest
from src.main import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_root_html(client):
    """Test that the root endpoint returns HTML when requested."""
    resp = client.get("/", headers={"Accept": "text/html"})
    assert resp.status_code == 200
    assert "text/html" in resp.content_type
    content = resp.data.decode('utf-8')
    assert "<!DOCTYPE html>" in content
    assert "Cuidar Plus API" in content
    assert "v1" in content  # Version check

    # Check for dark mode support
    assert "@media (prefers-color-scheme: dark)" in content
    assert "--bg-color: #121212" in content

    # Check for accessibility improvements
    assert '<span aria-hidden="true">📄</span>' in content
    assert '<span aria-hidden="true">💓</span>' in content

def test_root_json_default(client):
    """Test that the root endpoint returns JSON by default (no Accept header)."""
    resp = client.get("/")
    assert resp.status_code == 200
    assert "application/json" in resp.content_type
    data = resp.get_json()
    assert data["service"] == "Cuidar Plus API"
    assert "docs" in data

def test_root_json_explicit(client):
    """Test that the root endpoint returns JSON when explicitly requested."""
    resp = client.get("/", headers={"Accept": "application/json"})
    assert resp.status_code == 200
    assert "application/json" in resp.content_type
    data = resp.get_json()
    assert data["service"] == "Cuidar Plus API"

def test_root_json_wildcard(client):
    """Test that the root endpoint returns JSON for wildcard (*/*)."""
    resp = client.get("/", headers={"Accept": "*/*"})
    assert resp.status_code == 200
    assert "application/json" in resp.content_type
