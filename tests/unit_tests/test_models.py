import unittest
from app.models import User, Post

class UserModelCase(unittest.TestCase):
    
    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        
        self.assertTrue(u.check_password('cat'))
        self.assertFalse(u.check_password('dog'))

    def test_password_is_not_plaintext(self):
        u = User(username='john')
        u.set_password('wolf')
        self.assertNotEqual(u.password_hash, 'wolf')

    def test_avatar_generation(self):
        u = User(username='david', email='david@gmail.com')
        
        expected_hash = 'f3c52e5ef3d2b471d0ef51c66c21d10c'
        
        avatar_url = u.avatar(128)
        
        self.assertIn(expected_hash, avatar_url)
        self.assertIn('s=128', avatar_url)

    def test_user_repr(self):
        u = User(username='peter')
        self.assertEqual(repr(u), '<User peter>')

    def test_post_repr(self):
        p = Post(body='a sample post')
        self.assertEqual(repr(p), '<Post a sample post>')
