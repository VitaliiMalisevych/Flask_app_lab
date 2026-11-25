import pytest

from app import create_app, db
from app.users.models import User


@pytest.fixture
def client(tmp_path):
    app = create_app('development')
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        SQLALCHEMY_DATABASE_URI='sqlite:///' + str(tmp_path / 'test_lab9.sqlite'),
        SECRET_KEY='test-only-key'
    )
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def registration_data(username='student9', email='student9@example.com'):
    return {
        'username': username,
        'email': email,
        'password': 'Password123!',
        'confirm_password': 'Password123!'
    }


def test_pages_load(client):
    assert client.get('/users/register').status_code == 200
    assert client.get('/users/login').status_code == 200


def test_registration_saves_hashed_password(client):
    response = client.post('/users/register', data=registration_data(), follow_redirects=True)
    assert response.status_code == 200
    user = db.session.scalar(db.select(User).where(User.username == 'student9'))
    assert user is not None
    assert user.password != 'Password123!'
    assert user.password.startswith('$2')
    assert user.check_password('Password123!')


def test_duplicate_registration(client):
    client.post('/users/register', data=registration_data())
    response = client.post('/users/register', data=registration_data())
    assert 'вже існує'.encode('utf-8') in response.data


def test_login_logout_and_protected_pages(client):
    client.post('/users/register', data=registration_data())
    assert client.get('/users/account').status_code == 302
    assert client.get('/users/list').status_code == 302
    response = client.post('/users/login', data={'email': 'student9@example.com', 'password': 'Password123!'}, follow_redirects=True)
    assert response.status_code == 200
    assert 'student9'.encode('utf-8') in response.data
    assert client.get('/users/account').status_code == 200
    assert client.get('/users/list').status_code == 200
    client.get('/users/logout')
    assert client.get('/users/account').status_code == 302


def test_wrong_password(client):
    client.post('/users/register', data=registration_data())
    response = client.post('/users/login', data={'email': 'student9@example.com', 'password': 'wrong'})
    assert 'Неправильна'.encode('utf-8') in response.data
