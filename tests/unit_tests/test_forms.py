import unittest
from app import create_app
from app.auth.forms import LoginForm, RegistrationForm
from app.main.forms import EditProfileForm, PostForm

app = create_app()

class FormModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        self.request_context = app.test_request_context()
        self.request_context.push()

    def tearDown(self):
        self.request_context.pop()
        self.app_context.pop()

    def test_login_form_rejects_empty_fields(self):
        form = LoginForm(meta={'csrf': False})
        self.assertFalse(form.validate())
        self.assertTrue('username' in form.errors)
        self.assertTrue('password' in form.errors)

    def test_registration_form_rejects_mismatched_passwords(self):
        form = RegistrationForm(password='pass1', password2='pass2', meta={'csrf': False})
        self.assertFalse(form.validate())
        self.assertTrue('password2' in form.errors)
        self.assertIn('Field must be equal to password.', form.errors['password2'])

    def test_edit_profile_form_rejects_long_about_me(self):
        long_bio = ' | some text' * 100
        form = EditProfileForm('some_original_username', about_me=long_bio, meta={'csrf': False})
        self.assertFalse(form.validate())
        self.assertTrue('about_me' in form.errors)
        self.assertIn('Field must be between 0 and 140 characters long.', form.errors['about_me'])

    def test_post_form_rejects_empty_post(self):
        form = PostForm(post='', meta={'csrf': False})
        self.assertFalse(form.validate())
        self.assertTrue('post' in form.errors)
        self.assertIn('This field is required.', form.errors['post'])