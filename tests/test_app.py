import pytest
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that home page loads successfully"""
    rv = client.get('/')
    assert rv.status_code == 200

def test_api_data_without_token(client):
    """Test that API requires authentication"""
    rv = client.get('/api/data')
    assert rv.status_code == 401
