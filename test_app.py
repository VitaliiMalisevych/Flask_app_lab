
import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app('testing')

    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200


def test_resume_page(client):
    response = client.get('/resume')
    assert response.status_code == 200


def test_contact_page(client):
    response = client.get('/contact')
    assert response.status_code == 200


def test_products_list(client):
    response = client.get('/products/')
    assert response.status_code == 200


def test_add_product_page(client):
    response = client.get('/products/add')
    assert response.status_code == 200
