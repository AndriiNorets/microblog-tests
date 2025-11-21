from app.models import User
from app import db
import pytest

@pytest.fixture(scope='function')
def user2(app):
    with app.app_context():
        u = User(username='user_two', email='user2@example.com')
        db.session.add(u)
        db.session.commit()
        return u

def test_view_own_profile(client, user):
    client.post('/auth/login', data={'username': user.username, 'password': 'password'})
    response = client.get(f'/user/{user.username}')
    assert response.status_code == 200
    assert b'Edit your profile' in response.data

def test_edit_profile_success(client, user, app):
    client.post('/auth/login', data={'username': user.username, 'password': 'password'})
    response = client.post('/edit_profile', data={
        'username': 'new_username',
        'about_me': 'My new bio.'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Your changes have been saved.' in response.data

    with app.app_context():
        updated_user = db.session.get(User, user.id)
        assert updated_user.username == 'new_username'
        assert updated_user.about_me == 'My new bio.'

def test_follow_and_unfollow_user(client, user, user2, app):
    client.post('/auth/login', data={'username': user.username, 'password': 'password'})

    response_follow = client.post('/follow/user_two', follow_redirects=True)
    assert response_follow.status_code == 200
    assert b'you are following user_two' in response_follow.data.lower()

    with app.app_context():
        u1 = db.session.get(User, user.id)
        u2 = User.query.filter_by(username='user_two').first()
        
        assert u1 is not None
        assert u2 is not None
        assert u1.is_following(u2)

    response_unfollow = client.post('/unfollow/user_two', follow_redirects=True)
    assert response_unfollow.status_code == 200
    assert b'you are not following user_two' in response_unfollow.data.lower()

    with app.app_context():
        u1 = db.session.get(User, user.id)
        u2 = User.query.filter_by(username='user_two').first()

        assert u1 is not None
        assert u2 is not None
        assert not u1.is_following(u2)

def test_cannot_follow_self(client, user):
    client.post('/auth/login', data={'username': user.username, 'password': 'password'})
    response = client.post(f'/follow/{user.username}', follow_redirects=True)

    assert response.status_code == 200
    assert b'You cannot follow yourself!' in response.data