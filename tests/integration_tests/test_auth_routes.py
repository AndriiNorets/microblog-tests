from app.models import User

def test_registration_page_loads(client):
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b'Register' in response.data 

def test_successful_registration(client, app):
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'newuser@gmail.com',
        'password': 'password123',
        'password2': 'password123'
    }, follow_redirects=True) 

    assert response.status_code == 200
    assert b'Congratulations, you are now a registered user!' in response.data

    with app.app_context():
        user = User.query.filter_by(username='newuser').first()
        assert user is not None
        assert user.email == 'newuser@gmail.com'

def test_registration_with_duplicate_username(client, user):
    response = client.post('/auth/register', data={
        'username': 'testuser', 
        'email': 'another@gmail.com',
        'password': 'password123',
        'password2': 'password123'
    })

    assert response.status_code == 200
    assert b'Please use a different username.' in response.data

def test_registration_with_duplicate_email(client, user):
    response = client.post('/auth/register', data={
        'username': 'anotheruser',
        'email': 'test@gmail.com',
        'password': 'password123',
        'password2': 'password123'
    })
    assert response.status_code == 200
    assert b'Please use a different email address.' in response.data

def test_registration_with_password_mismatch(client):
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'newuser@gmail.com',
        'password': 'password123',
        'password2': 'WrongPassword'
    })

    assert response.status_code == 200
    assert b'Field must be equal to password.' in response.data

# LOGIN

def test_login_page_loads(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'<h1>Sign In</h1>' in response.data

def test_successful_login(client, user):
    response = client.post('/auth/login', data={
        'username': user.username, # 'testuser'
        'password': 'password'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Logout' in response.data
    assert b'Login' not in response.data

def test_login_with_invalid_username(client):
    response = client.post('/auth/login', data={
        'username': 'nonexistentuser',
        'password': 'anypassword'
    }, follow_redirects=True) 

    assert response.status_code == 200
    assert b'Invalid username or password' in response.data
    assert b'Logout' not in response.data

def test_login_with_wrong_password(client, user):
    response = client.post('/auth/login', data={
        'username': user.username,
        'password': 'wrongpassword'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data
    assert b'Logout' not in response.data

def test_user_logout(client, user):
    client.post('/auth/login', data={
        'username': user.username,
        'password': 'password'
    }, follow_redirects=True)

    response = client.get('/auth/logout', follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Logout' not in response.data