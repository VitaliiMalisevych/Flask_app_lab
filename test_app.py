import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_contact_page_get(client):
    response = client.get('/contact')
    assert response.status_code == 200

def test_contact_page_post(client):
    response = client.post('/contact', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'phone': '+380991234567',
        'subject': 'Тест',
        'message': 'Тестове повідомлення'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_products_list(client):
    response = client.get('/products/')
    assert response.status_code == 200

def test_add_product_page(client):
    response = client.get('/products/add')
    assert response.status_code == 200