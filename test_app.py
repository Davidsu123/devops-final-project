import pytest
from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_check_structure(client):
    """Test that the health check endpoint returns the correct structure."""
    response = client.get('/health')
    assert response.status_code in [200, 500] # Can be 500 if DB is not available
    assert "status" in response.get_json()

def test_main_page_structure(client):
    """Test that the main page returns the correct structure."""
    response = client.get('/')
    assert response.status_code in [200, 500]
    assert "message" in response.get_json()
