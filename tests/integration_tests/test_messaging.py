from app.models import User, Message
from app import db
import pytest

@pytest.fixture(scope='function')
def user2(app):
    with app.app_context():
        u = User(username='user_two', email='user2@example.com')
        db.session.add(u)
        db.session.commit()
        return u

def test_inbox_shows_received_messages(client, user, user2, app):

    with app.app_context():
        u1 = db.session.get(User, user.id)
        u2 = User.query.filter_by(username='user_two').first()
        
        assert u1 is not None
        assert u2 is not None

        message_text = "Hello from user_two!"
        msg = Message(author=u2, recipient=u1, body=message_text)
        db.session.add(msg)
        db.session.commit()

    client.post('/auth/login', data={'username': user.username, 'password': 'password'})

    response = client.get('/messages')

    assert response.status_code == 200
    assert b'user_two' in response.data
    assert bytes(message_text, 'utf-8') in response.data


def test_inbox_only_shows_received_not_sent(client, user, user2, app):
    with app.app_context():
        u1 = db.session.get(User, user.id)
        u2 = User.query.filter_by(username='user_two').first()

        assert u1 is not None
        assert u2 is not None

        received_text = "This is a message for me."
        msg1 = Message(author=u2, recipient=u1, body=received_text)

        sent_text = "This is a message from me."
        msg2 = Message(author=u1, recipient=u2, body=sent_text)
        
        db.session.add_all([msg1, msg2])
        db.session.commit()

    client.post('/auth/login', data={'username': user.username, 'password': 'password'})

    response = client.get('/messages')
    assert response.status_code == 200

    assert bytes(received_text, 'utf-8') in response.data
    assert bytes(sent_text, 'utf-8') not in response.data