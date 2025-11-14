from app.models import User, Post
from app import db
import pytest
from datetime import datetime, timezone, timedelta

@pytest.fixture(scope='function')
def user2(app):
    with app.app_context():
        u = User(username='user_two', email='user2@example.com')
        db.session.add(u)
        db.session.commit()
        return u

def test_create_post_success(client, user, app):
    client.post('/auth/login', data={'username': user.username, 'password': 'password'})

    post_text = 'This is my first test post!'
    response = client.post('/', data={'post': post_text}, follow_redirects=True)

    assert response.status_code == 200
    assert bytes(post_text, 'utf-8') in response.data

    with app.app_context():
        p = Post.query.filter_by(body=post_text).first()
        assert p is not None
        assert p.author.id == user.id

def test_create_post_empty_body_error(client, user):
    client.post('/auth/login', data={'username': user.username, 'password': 'password'})
    response = client.post('/', data={'post': ''}, follow_redirects=True)

    assert response.status_code == 200
    assert b'Your post is now live!' not in response.data

def test_timeline_shows_followed_user_posts(client, user, user2, app):
    with app.app_context():
        u1 = db.session.get(User, user.id)
        u2 = User.query.filter_by(username='user_two').first()

        assert u1 is not None
        assert u2 is not None

        u1.follow(u2)

        post_by_user2 = Post(body="A post by user_two.", author=u2)
        db.session.add(post_by_user2)
        db.session.commit()

    client.post('/auth/login', data={'username': user.username, 'password': 'password'})

    response = client.get('/')

    assert response.status_code == 200
    assert b'A post by user_two.' in response.data
