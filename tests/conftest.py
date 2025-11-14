import pytest
from app import create_app, db
from app.models import User
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False
    ELASTICSEARCH_URL = None

@pytest.fixture(scope='function') 
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function') 
def client(app):
    return app.test_client()

@pytest.fixture(scope='function') 
def user(app, client, db_session):
    u = User(username='testuser', email='test@gmail.com')
    u.set_password('password')
    db_session.add(u)
    db_session.commit()
    return u

@pytest.fixture(scope='function')
def db_session(app, request):
    with app.app_context():
        yield db.session