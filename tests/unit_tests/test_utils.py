import unittest
from unittest.mock import patch
from app import create_app
from app.email import send_email
from app.translate import translate

app = create_app()

class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.email.mail.send')
    def test_send_email_function_creates_correct_message(self, mock_mail_send):

        send_email('Test Subject',
                   sender='sender@gmail.com',
                   recipients=['recipient@gmail.com'],
                   text_body='This is a test.',
                   html_body='<p>This is a test.</p>')

        self.assertTrue(mock_mail_send.called)
        
        sent_message = mock_mail_send.call_args[0][0]
        
        self.assertEqual(sent_message.subject, 'Test Subject')
        self.assertEqual(sent_message.sender, 'sender@gmail.com')
        self.assertEqual(sent_message.recipients, ['recipient@gmail.com'])
        self.assertEqual(sent_message.body, 'This is a test.')
        self.assertEqual(sent_message.html, '<p>This is a test.</p>')

    def test_translate_function_handles_no_key_error(self):

        with app.test_request_context():
            app.config['MS_TRANSLATOR_KEY'] = None

            translation_result = translate('Hello', 'en', 'es')
            self.assertIn('Error: the translation service is not configured.', str(translation_result))