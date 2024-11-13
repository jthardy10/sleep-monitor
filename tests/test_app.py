import pytest
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that home page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200

def test_api_token_endpoint(client):
    """Test that token endpoint returns successful response"""
    response = client.post('/api/token')
    assert response.status_code == 200
