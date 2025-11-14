import pytest
from config import Config
from app import create_app, db
from app.models import User
import json

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

app = create_app(TestConfig)

@pytest.fixture
def auth_headers(client, user):
    token = user.get_token()
    return {'Authorization': f'Bearer {token}'}


def test_users_endpoint2(client, auth_headers):
    response = client.get('/api/users', headers=auth_headers)
    assert response.status_code == 200
    assert 'testuser' in response.get_data(as_text=True)


def test_get_user2(client, auth_headers, user):
    response = client.get(f'/api/users/{user.id}', headers=auth_headers)
    assert response.status_code == 200
    assert 'testuser' in response.get_data(as_text=True)

def test_api_create_user(client):
    response = client.post('/api/users', 
        data=json.dumps({
            'username': 'api_user',
            'email': 'api@gmail.com',
            'password': 'password'
        }),
        content_type='application/json'
    )
    assert response.status_code == 201 
    assert 'api_user' in str(response.data)

def test_api_create_user_duplicate_email(client, user):

    response = client.post('/api/users', 
        data=json.dumps({
            'username': 'another_api_user',
            'email': user.email, 
            'password': 'password'
        }),
        content_type='application/json'
    )
    assert response.status_code == 400 
    assert b'please use a different email address' in response.data.lower()

def test_api_update_user(client, user, auth_headers, app):
    response = client.put(f'/api/users/{user.id}', 
        headers=auth_headers,
        data=json.dumps({
            'about_me': 'This is my new bio via API'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    assert b'This is my new bio via API' in response.data

    with app.app_context():
        updated_user = db.session.get(User, user.id)
        assert updated_user.about_me == 'This is my new bio via API'